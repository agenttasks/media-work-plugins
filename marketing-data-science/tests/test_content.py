"""Tests for content extraction, briefs, and calendar models."""

from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from models.content import (
    ChangelogEntry,
    ContentBrief,
    ContentCalendar,
    ContentPillar,
    ImpactLevel,
    PlatformAdaptation,
    ScriptFramework,
)


class TestChangelogEntry:
    @pytest.mark.parametrize("cat", ["feature", "bugfix", "breaking", "performance"])
    def test_valid_categories(self, cat):
        entry = ChangelogEntry(
            changelog_date=date(2025, 3, 1),
            category=cat,
            title="Test",
            description="desc",
            impact_level=ImpactLevel.LOW,
        )
        assert entry.category == cat

    def test_invalid_category_rejected(self):
        with pytest.raises(ValidationError):
            ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category="enhancement",
                title="Test",
                description="desc",
                impact_level=ImpactLevel.LOW,
            )

    @pytest.mark.parametrize(
        "title,should_fail",
        [("", True), ("x" * 201, True), ("x" * 200, False), ("Valid title", False)],
    )
    def test_title_length_bounds(self, title, should_fail):
        if should_fail:
            with pytest.raises(ValidationError):
                ChangelogEntry(
                    changelog_date=date(2025, 3, 1),
                    category="feature",
                    title=title,
                    description="desc",
                    impact_level=ImpactLevel.HIGH,
                )
        else:
            entry = ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category="feature",
                title=title,
                description="desc",
                impact_level=ImpactLevel.HIGH,
            )
            assert entry.title == title

    def test_source_reference_optional(self):
        base = dict(
            changelog_date=date(2025, 3, 1),
            category="bugfix",
            title="Fix crash",
            description="desc",
            impact_level=ImpactLevel.MEDIUM,
        )
        assert ChangelogEntry(**base).source_reference is None
        assert ChangelogEntry(**base, source_reference="abc123").source_reference == "abc123"


class TestPlatformAdaptation:
    def test_valid_adaptation(self):
        pa = PlatformAdaptation(platform="instagram", script="Demo script", duration_seconds=30)
        assert pa.duration_seconds == 30

    @pytest.mark.parametrize("dur,valid", [(14, False), (15, True), (60, True), (90, True), (91, False)])
    def test_duration_boundaries(self, dur, valid):
        if valid:
            pa = PlatformAdaptation(platform="tiktok", script="X", duration_seconds=dur)
            assert pa.duration_seconds == dur
        else:
            with pytest.raises(ValidationError):
                PlatformAdaptation(platform="instagram", script="Demo", duration_seconds=dur)

    def test_empty_script_rejected(self):
        with pytest.raises(ValidationError):
            PlatformAdaptation(platform="instagram", script="", duration_seconds=30)


class TestScriptFramework:
    def test_valid_script(self, sample_script):
        assert sample_script.hook == "Check this out"

    def test_hook_under_20_words(self):
        hook = " ".join(["word"] * 20)
        script = ScriptFramework(hook=hook, context="Ctx", demo="Demo", cta="CTA")
        assert len(script.hook.split()) == 20

    def test_hook_over_20_words_rejected(self):
        with pytest.raises(ValidationError, match="keep under 20"):
            ScriptFramework(hook=" ".join(["a"] * 21), context="Ctx", demo="Demo", cta="CTA")

    @pytest.mark.parametrize(
        "field,length", [("hook", 101), ("cta", 151)]
    )
    def test_max_length_exceeded(self, field, length):
        kwargs = dict(hook="Hook", context="Context", demo="Demo", cta="CTA")
        kwargs[field] = "x" * length
        with pytest.raises(ValidationError):
            ScriptFramework(**kwargs)


def _make_brief(**overrides):
    defaults = dict(
        changelog_entry=ChangelogEntry(
            changelog_date=date(2025, 3, 1),
            category="feature",
            title="Test feature",
            description="desc",
            impact_level=ImpactLevel.HIGH,
        ),
        headline="Big Feature Drop",
        content_pillar=ContentPillar.FEATURE_DROPS,
        script=ScriptFramework(hook="Check this out", context="Ctx", demo="Demo", cta="Try it"),
        platforms={
            p: PlatformAdaptation(platform=p, script="Script", duration_seconds=30)
            for p in ("instagram", "tiktok", "youtube")
        },
        hashtags=["#feature", "#update"],
    )
    defaults.update(overrides)
    return ContentBrief(**defaults)


class TestContentBrief:
    def test_valid_brief(self):
        assert len(_make_brief().platforms) == 3

    @pytest.mark.parametrize(
        "platforms,error",
        [
            ({"instagram": None, "tiktok": None}, "Missing platform adaptations"),
            ({}, "Missing platform adaptations"),
        ],
    )
    def test_missing_platform_rejected(self, platforms, error):
        real_platforms = {
            k: PlatformAdaptation(platform=k, script="Script", duration_seconds=30)
            for k in platforms
        }
        with pytest.raises(ValidationError, match=error):
            _make_brief(platforms=real_platforms)

    def test_invalid_hashtag_format(self):
        with pytest.raises(ValidationError, match="Hashtag must start with #"):
            _make_brief(hashtags=["#valid", "invalid"])

    def test_all_hashtags_valid(self):
        brief = _make_brief(hashtags=["#one", "#two", "#three"])
        assert all(t.startswith("#") for t in brief.hashtags)

    def test_empty_hashtags_rejected(self):
        with pytest.raises(ValidationError):
            _make_brief(hashtags=[])


class TestContentCalendar:
    def _make_calendar(self, **overrides):
        defaults = dict(week_start=date(2025, 3, 3), briefs=[_make_brief()], posting_schedule={})
        defaults.update(overrides)
        return ContentCalendar(**defaults)

    def test_valid_calendar(self):
        cal = self._make_calendar()
        assert cal.week_start == date(2025, 3, 3)

    def test_empty_briefs_rejected(self):
        with pytest.raises(ValidationError):
            ContentCalendar(week_start=date(2025, 3, 3), briefs=[])

    def test_duplicate_platform_day_rejected(self):
        schedule = {
            "instagram": [
                {"brief_index": 0, "scheduled_date": date(2025, 3, 3)},
                {"brief_index": 1, "scheduled_date": date(2025, 3, 3)},
            ]
        }
        with pytest.raises(ValidationError, match="Duplicate post"):
            self._make_calendar(posting_schedule=schedule)

    def test_different_days_allowed(self):
        schedule = {
            "instagram": [
                {"brief_index": 0, "scheduled_date": date(2025, 3, 3)},
                {"brief_index": 1, "scheduled_date": date(2025, 3, 4)},
            ]
        }
        cal = self._make_calendar(posting_schedule=schedule)
        assert len(cal.posting_schedule["instagram"]) == 2
