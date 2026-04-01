"""Pydantic models for cross-plugin requirements handoff between marketing-data-science and platform-engineering."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from .base import Platform


class RequirementStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    BLOCKED = "blocked"
    REJECTED = "rejected"


class RequirementType(StrEnum):
    VIDEO_GENERATION = "video_generation"
    CONTENT_UPLOAD = "content_upload"
    INTEGRATION_SETUP = "integration_setup"
    MEASUREMENT_PIPELINE = "measurement_pipeline"


class Priority(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


Duration = Annotated[int, Field(ge=15, le=90)]
Visibility = Literal["public", "private", "unlisted"]
MaxHashtags = Annotated[list[str], Field(max_length=30)]


class ContentSpec(BaseModel):
    """Content specification for video generation."""

    platform: Platform
    duration_seconds: Duration
    aspect_ratio: str = "9:16"
    resolution: str = "1080x1920"
    script: str = Field(min_length=1)
    visual_style: str = ""
    audio: Literal["voiceover", "trending_sound", "original"] = "voiceover"

    @field_validator("resolution")
    @classmethod
    def validate_resolution(cls, v: str) -> str:
        try:
            w, h = v.split("x")
            int(w)
            int(h)
        except (ValueError, AttributeError) as err:
            raise ValueError(f"Resolution must be WxH format: {v}") from err
        return v


class VideoGenerationSpec(BaseModel):
    """Higgsfield video generation parameters."""

    provider: str = "higgsfield"
    style: str
    avatar_id: str | None = None
    lip_sync: bool = False
    camera_controls: str | None = None
    upscale: bool = False
    additional_params: dict[str, Any] = Field(default_factory=dict)


class UploadSpec(BaseModel):
    """Platform-specific upload specification."""

    platform: Platform
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(max_length=5000)
    hashtags: MaxHashtags = []
    scheduled_time: datetime | None = None
    visibility: Visibility = "public"


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
    source_skill: str
    priority: Priority
    type: RequirementType
    status: RequirementStatus = RequirementStatus.PENDING

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
        if self.type == RequirementType.VIDEO_GENERATION and (
            self.content_spec is None or self.video_generation is None
        ):
            raise ValueError(
                "VIDEO_GENERATION requirements need content_spec and video_generation"
            )
        if self.type == RequirementType.CONTENT_UPLOAD and self.upload_spec is None:
            raise ValueError("CONTENT_UPLOAD requirements need upload_spec")
        return self

    @model_validator(mode="after")
    def validate_blocked_reason(self) -> Requirement:
        if self.status == RequirementStatus.BLOCKED and not self.blocked_reason:
            raise ValueError("Blocked requirements must have a blocked_reason")
        if self.status == RequirementStatus.REJECTED and not self.rejected_reason:
            raise ValueError("Rejected requirements must have a rejected_reason")
        return self
