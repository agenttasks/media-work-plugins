"""Pydantic models for cross-plugin requirements handoff between marketing-data-science and platform-engineering."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from .base import Platform


class RequirementStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    BLOCKED = "blocked"
    REJECTED = "rejected"


class RequirementType(str, Enum):
    VIDEO_GENERATION = "video_generation"
    CONTENT_UPLOAD = "content_upload"
    INTEGRATION_SETUP = "integration_setup"
    MEASUREMENT_PIPELINE = "measurement_pipeline"


class Priority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class ContentSpec(BaseModel):
    """Content specification for video generation."""

    platform: Platform
    duration_seconds: int = Field(ge=15, le=90)
    aspect_ratio: str = Field(default="9:16")
    resolution: str = Field(default="1080x1920")
    script: str = Field(min_length=1)
    visual_style: str = ""
    audio: str = Field(default="voiceover", description="voiceover | trending_sound | original")

    @field_validator("resolution")
    @classmethod
    def validate_resolution(cls, v: str) -> str:
        try:
            w, h = v.split("x")
            int(w)
            int(h)
        except (ValueError, AttributeError):
            raise ValueError(f"Resolution must be WxH format: {v}")
        return v


class VideoGenerationSpec(BaseModel):
    """Higgsfield video generation parameters."""

    provider: str = Field(default="higgsfield")
    style: str = Field(description="e.g. talking_avatar, screen_recording, text_overlay")
    avatar_id: str | None = None
    lip_sync: bool = False
    camera_controls: str | None = Field(
        default=None, description="e.g. zoom_in, pan_left, static"
    )
    upscale: bool = Field(default=False, description="Upscale output via Higgsfield")
    additional_params: dict[str, Any] = Field(default_factory=dict)


class UploadSpec(BaseModel):
    """Platform-specific upload specification."""

    platform: Platform
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(max_length=5000)
    hashtags: list[str] = Field(default_factory=list)
    scheduled_time: datetime | None = None
    visibility: str = Field(default="public")

    @field_validator("visibility")
    @classmethod
    def validate_visibility(cls, v: str) -> str:
        allowed = {"public", "private", "unlisted"}
        if v not in allowed:
            raise ValueError(f"visibility must be one of {allowed}")
        return v

    @field_validator("hashtags")
    @classmethod
    def validate_hashtag_count(cls, v: list[str]) -> list[str]:
        if len(v) > 30:
            raise ValueError("Maximum 30 hashtags allowed (Instagram limit)")
        return v


class ExperimentTracking(BaseModel):
    """Experiment tracking metadata attached to requirements."""

    experiment_id: UUID | None = None
    variant: str | None = Field(default=None, pattern="^[AB]$")
    tracking_params: dict[str, Any] = Field(default_factory=dict)


class Requirement(BaseModel):
    """
    A structured requirement handed off from marketing-data-science to platform-engineering.

    This is the primary cross-plugin communication contract.
    """

    requirement_id: UUID = Field(default_factory=uuid4)
    source_skill: str = Field(description="Originating skill name")
    priority: Priority
    type: RequirementType
    status: RequirementStatus = Field(default=RequirementStatus.PENDING)

    content_spec: ContentSpec | None = None
    video_generation: VideoGenerationSpec | None = None
    upload_spec: UploadSpec | None = None
    experiment: ExperimentTracking = Field(default_factory=ExperimentTracking)

    acceptance_criteria: list[str] = Field(default_factory=list, min_length=1)
    blocked_reason: str | None = None
    rejected_reason: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_spec_for_type(self) -> Requirement:
        """Ensure the right specs are provided for the requirement type."""
        if self.type == RequirementType.VIDEO_GENERATION:
            if self.content_spec is None or self.video_generation is None:
                raise ValueError(
                    "VIDEO_GENERATION requirements need content_spec and video_generation"
                )
        if self.type == RequirementType.CONTENT_UPLOAD:
            if self.upload_spec is None:
                raise ValueError("CONTENT_UPLOAD requirements need upload_spec")
        return self

    @model_validator(mode="after")
    def validate_blocked_reason(self) -> Requirement:
        if self.status == RequirementStatus.BLOCKED and not self.blocked_reason:
            raise ValueError("Blocked requirements must have a blocked_reason")
        if self.status == RequirementStatus.REJECTED and not self.rejected_reason:
            raise ValueError("Rejected requirements must have a rejected_reason")
        return self
