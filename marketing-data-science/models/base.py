"""Base Pydantic models providing session context and telemetry for all marketing-data-science skills."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator


class Platform(StrEnum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


NonNegativeFloat = Annotated[float, Field(ge=0.0)]
NonNegativeInt = Annotated[int, Field(ge=0)]


class DeviceSurface(BaseModel):
    """Detected device capabilities at session start."""

    available_mcp_servers: list[str] = []
    local_tools: list[str] = []
    configured_api_keys: list[str] = []
    platform_engineering_available: bool = False


class TelemetryEvent(BaseModel):
    """Structured telemetry event emitted by all skills."""

    session_id: str
    skill_name: str
    event_type: str
    platform: Platform | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cost_usd: NonNegativeFloat = 0.0
    tokens_used: NonNegativeInt = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class BaseSessionContext(BaseModel):
    """
    Base session context inherited by all marketing-data-science models.

    Provides canonical Claude Code session metadata: session ID, costs,
    telemetry, logging, device surface, and lifecycle touch points.
    """

    session_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    device_surface: DeviceSurface = Field(default_factory=DeviceSurface)
    total_cost_usd: NonNegativeFloat = 0.0
    total_tokens_used: NonNegativeInt = 0
    telemetry_events: list[TelemetryEvent] = Field(default_factory=list)
    log_level: LogLevel = LogLevel.INFO

    def emit_telemetry(self, skill_name: str, event_type: str, **kwargs: Any) -> TelemetryEvent:
        """Create and record a telemetry event."""
        event = TelemetryEvent(
            session_id=self.session_id,
            skill_name=skill_name,
            event_type=event_type,
            **kwargs,
        )
        self.telemetry_events.append(event)
        return event

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("session_id must not be empty")
        return v.strip()
