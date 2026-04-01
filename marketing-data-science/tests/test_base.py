"""Tests for base session context and telemetry models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from models.base import (
    BaseSessionContext,
    DeviceSurface,
    LogLevel,
    Platform,
    TelemetryEvent,
)


class TestPlatformEnum:
    def test_values(self):
        assert Platform.INSTAGRAM == "instagram"
        assert Platform.TIKTOK == "tiktok"
        assert Platform.YOUTUBE == "youtube"

    def test_invalid_platform(self):
        with pytest.raises(ValueError):
            Platform("snapchat")


class TestDeviceSurface:
    def test_defaults(self):
        surface = DeviceSurface()
        assert surface.available_mcp_servers == []
        assert surface.local_tools == []
        assert surface.configured_api_keys == []
        assert surface.platform_engineering_available is False

    def test_custom_values(self):
        surface = DeviceSurface(
            available_mcp_servers=["higgsfield"],
            local_tools=["ffmpeg"],
            configured_api_keys=["HIGGSFIELD_API_KEY"],
            platform_engineering_available=True,
        )
        assert surface.available_mcp_servers == ["higgsfield"]
        assert surface.platform_engineering_available is True


class TestTelemetryEvent:
    def test_create_event(self):
        event = TelemetryEvent(
            session_id="sess-123",
            skill_name="content-strategy",
            event_type="content_generated",
        )
        assert event.session_id == "sess-123"
        assert event.cost_usd == 0.0
        assert event.tokens_used == 0
        assert event.metadata == {}

    def test_with_platform(self):
        event = TelemetryEvent(
            session_id="sess-123",
            skill_name="content-strategy",
            event_type="content_generated",
            platform=Platform.INSTAGRAM,
        )
        assert event.platform == Platform.INSTAGRAM

    @pytest.mark.parametrize("field,value", [("cost_usd", -1.0), ("tokens_used", -10)])
    def test_negative_values_rejected(self, field, value):
        with pytest.raises(ValidationError):
            TelemetryEvent(
                session_id="sess-123", skill_name="test", event_type="test", **{field: value}
            )


class TestBaseSessionContext:
    def test_valid_session(self):
        ctx = BaseSessionContext(session_id="sess-abc")
        assert ctx.session_id == "sess-abc"
        assert ctx.total_cost_usd == 0.0
        assert ctx.log_level == LogLevel.INFO

    @pytest.mark.parametrize("sid", ["", "   "])
    def test_empty_or_whitespace_session_id_rejected(self, sid):
        with pytest.raises(ValidationError, match="session_id must not be empty"):
            BaseSessionContext(session_id=sid)

    def test_session_id_stripped(self):
        ctx = BaseSessionContext(session_id="  sess-123  ")
        assert ctx.session_id == "sess-123"

    def test_emit_telemetry(self):
        ctx = BaseSessionContext(session_id="sess-123")
        event = ctx.emit_telemetry("content-strategy", "content_generated")
        assert len(ctx.telemetry_events) == 1
        assert event.session_id == "sess-123"
        assert event.skill_name == "content-strategy"

    def test_emit_telemetry_with_kwargs(self):
        ctx = BaseSessionContext(session_id="sess-123")
        event = ctx.emit_telemetry(
            "content-strategy",
            "content_generated",
            platform=Platform.TIKTOK,
            cost_usd=0.05,
            tokens_used=150,
        )
        assert event.platform == Platform.TIKTOK
        assert event.cost_usd == 0.05
        assert event.tokens_used == 150

    def test_emit_multiple_events(self):
        ctx = BaseSessionContext(session_id="sess-123")
        for name in ("skill-a", "skill-b", "skill-c"):
            ctx.emit_telemetry(name, f"event_{name[-1]}")
        assert len(ctx.telemetry_events) == 3

    def test_negative_total_cost_rejected(self):
        with pytest.raises(ValidationError):
            BaseSessionContext(session_id="sess-123", total_cost_usd=-5.0)
