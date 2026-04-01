"""Pydantic models for content extraction, briefs, and calendar management."""

from __future__ import annotations

from datetime import date, datetime, time
from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ImpactLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContentPillar(StrEnum):
    FEATURE_DROPS = "feature_drops"
    TIPS_AND_TRICKS = "tips_and_tricks"
    BEFORE_AFTER = "before_after"
    COMMUNITY_WINS = "community_wins"


Category = Literal["feature", "bugfix", "breaking", "performance"]
Duration = Annotated[int, Field(ge=15, le=90)]


class ChangelogEntry(BaseModel):
    """A single parsed entry from anthropics/claude-code CHANGELOG.md."""

    changelog_date: date
    category: Category
    title: str = Field(min_length=1, max_length=200)
    description: str
    impact_level: ImpactLevel
    source_reference: str | None = None


class PlatformAdaptation(BaseModel):
    """Platform-specific content adaptation."""

    platform: str
    script: str = Field(min_length=1)
    duration_seconds: Duration
    style_notes: str = ""
    hashtags: list[str] = []
    posting_time: time | None = None


class ScriptFramework(BaseModel):
    """Structured script following the HOOK-CONTEXT-DEMO-CTA framework."""

    hook: str = Field(max_length=100)
    context: str = Field(description="3-10 seconds, what changed and why")
    demo: str = Field(description="10-35 seconds, show feature in action")
    cta: str = Field(max_length=150)

    @field_validator("hook")
    @classmethod
    def validate_hook_length(cls, v: str) -> str:
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
    platforms: dict[str, PlatformAdaptation]
    hashtags: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_platforms(self) -> ContentBrief:
        missing = {"instagram", "tiktok", "youtube"} - set(self.platforms.keys())
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
    posting_schedule: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_no_duplicate_platform_day(self) -> ContentCalendar:
        """Ensure no platform gets duplicate content on the same day."""
        seen: set[tuple[str, date]] = set()
        for platform, posts in self.posting_schedule.items():
            for post in posts:
                if "scheduled_date" in post:
                    key = (platform, post["scheduled_date"])
                    if key in seen:
                        raise ValueError(
                            f"Duplicate post on {platform} for {post['scheduled_date']}"
                        )
                    seen.add(key)
        return self
