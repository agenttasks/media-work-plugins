"""Pydantic models for content extraction, briefs, and calendar management."""

from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class ImpactLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContentPillar(str, Enum):
    FEATURE_DROPS = "feature_drops"
    TIPS_AND_TRICKS = "tips_and_tricks"
    BEFORE_AFTER = "before_after"
    COMMUNITY_WINS = "community_wins"


class ChangelogEntry(BaseModel):
    """A single parsed entry from anthropics/claude-code CHANGELOG.md."""

    changelog_date: date
    category: str = Field(description="feature | bugfix | breaking | performance")
    title: str = Field(min_length=1, max_length=200)
    description: str
    impact_level: ImpactLevel
    source_reference: str | None = Field(
        default=None, description="Commit SHA or PR number"
    )

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = {"feature", "bugfix", "breaking", "performance"}
        if v not in allowed:
            raise ValueError(f"category must be one of {allowed}")
        return v


class PlatformAdaptation(BaseModel):
    """Platform-specific content adaptation."""

    platform: str
    script: str = Field(min_length=1)
    duration_seconds: int = Field(ge=15, le=90)
    style_notes: str = ""
    hashtags: list[str] = Field(default_factory=list)
    posting_time: time | None = None

    @field_validator("duration_seconds")
    @classmethod
    def validate_duration(cls, v: int) -> int:
        if v > 60 and v != 90:
            # Instagram allows up to 90s, others cap at 60s
            pass
        return v


class ScriptFramework(BaseModel):
    """Structured script following the HOOK-CONTEXT-DEMO-CTA framework."""

    hook: str = Field(description="0-3 seconds, attention grabber", max_length=100)
    context: str = Field(description="3-10 seconds, what changed and why")
    demo: str = Field(description="10-35 seconds, show feature in action")
    cta: str = Field(description="35-45 seconds, call to action", max_length=150)

    @field_validator("hook")
    @classmethod
    def validate_hook_length(cls, v: str) -> str:
        # Approximate 3-second read time at ~150 WPM = ~7-8 words
        word_count = len(v.split())
        if word_count > 20:
            raise ValueError(f"Hook has {word_count} words; keep under 20 for 3-second read time")
        return v


class ContentBrief(BaseModel):
    """Complete content brief generated from a CHANGELOG entry."""

    changelog_entry: ChangelogEntry
    headline: str = Field(min_length=1, max_length=100)
    content_pillar: ContentPillar
    script: ScriptFramework
    platforms: dict[str, PlatformAdaptation] = Field(
        description="Platform-specific adaptations keyed by platform name"
    )
    hashtags: list[str] = Field(default_factory=list, min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_platforms(self) -> ContentBrief:
        required = {"instagram", "tiktok", "youtube"}
        provided = set(self.platforms.keys())
        missing = required - provided
        if missing:
            raise ValueError(f"Missing platform adaptations: {missing}")
        return self

    @field_validator("hashtags")
    @classmethod
    def validate_hashtags(cls, v: list[str]) -> list[str]:
        for tag in v:
            if not tag.startswith("#"):
                raise ValueError(f"Hashtag must start with #: {tag}")
        return v


class ContentCalendar(BaseModel):
    """7-day rolling content calendar."""

    week_start: date
    briefs: list[ContentBrief] = Field(min_length=1)
    posting_schedule: dict[str, list[dict[str, Any]]] = Field(
        default_factory=dict,
        description="Platform -> list of {brief_index, scheduled_time}",
    )

    @model_validator(mode="after")
    def validate_no_duplicate_platform_day(self) -> ContentCalendar:
        """Ensure no platform gets duplicate content on the same day."""
        seen: dict[tuple[str, date], int] = {}
        for platform, posts in self.posting_schedule.items():
            for post in posts:
                if "scheduled_date" in post:
                    key = (platform, post["scheduled_date"])
                    if key in seen:
                        raise ValueError(
                            f"Duplicate post on {platform} for {post['scheduled_date']}"
                        )
                    seen[key] = 1
        return self
