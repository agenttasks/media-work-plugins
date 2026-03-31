"""Tests for content extraction, briefs, and calendar models."""

from __future__ import annotations

from datetime import date, datetime

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
    def test_valid_categories(self):
        for cat in ("feature", "bugfix", "breaking", "performance"):
            entry = ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category=cat,
                title="Test",
                description="desc",
                impact_level=ImpactLevel.LOW,
            )
            assert entry.category == cat

    def test_invalid_category_rejected(self):
        with pytest.raises(ValidationError, match="category must be one of"):
            ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category="enhancement",
                title="Test",
                description="desc",
                impact_level=ImpactLevel.LOW,
            )

    def test_empty_title_rejected(self):
        with pytest.raises(ValidationError):
            ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category="feature",
                title="",
                description="desc",
                impact_level=ImpactLevel.HIGH,
            )

    def test_title_max_length(self):
        with pytest.raises(ValidationError):
            ChangelogEntry(
                changelog_date=date(2025, 3, 1),
                category="feature",
                title="x" * 201,
                description="desc",
                impact_level=ImpactLevel.HIGH,
            )

    def test_title_at_max_length(self):
        entry = ChangelogEntry(
            changelog_date=date(2025, 3, 1),
            category="feature",
            title="x" * 200,
            description="desc",
            impact_level=ImpactLevel.HIGH,
        )
        assert len(entry.title) == 200

    def test_source_reference_optional(self):
        entry = ChangelogEntry(
            changelog_date=date(2025, 3, 1),
            category="bugfix",
            title="Fix crash",
            description="desc",
            impact_level=ImpactLevel.MEDIUM,
        )
        assert entry.source_reference is None

        entry_with_ref = ChangelogEntry(
            changelog_date=date(2025, 3, 1),
            category="bugfix",
            title="Fix crash",
            description="desc",
            impact_level=ImpactLevel.MEDIUM,
            source_reference="abc123",
        )
        assert entry_with_ref.source_reference == "abc123"


class TestPlatformAdaptation:
    def test_valid_adaptation(self):
        pa = PlatformAdaptation(
            platform="instagram",
            script="Demo script",
            duration_seconds=30,
        )
        assert pa.duration_seconds == 30

    def test_duration_minimum(self):
        with pytest.raises(ValidationError):
            PlatformAdaptation(
                platform="instagram",
                script="Demo",
                duration_seconds=14,
            )

    def test_duration_maximum(self):
        with pytest.raises(ValidationError):
            PlatformAdaptation(
                platform="instagram",
                script="Demo",
                duration_seconds=91,
            )

    def test_duration_boundary_15(self):
        pa = PlatformAdaptation(platform="tiktok", script="X", duration_seconds=15)
        assert pa.duration_seconds == 15

    def test_duration_boundary_60(self):
        pa = PlatformAdaptation(platform="tiktok", script="X", duration_seconds=60)
        assert pa.duration_seconds == 60

    def test_duration_boundary_90(self):
        pa = PlatformAdaptation(platform="instagram", script="X", duration_seconds=90)
        assert pa.duration_seconds == 90

    def test_empty_script_rejected(self):
        with pytest.raises(ValidationError):
            PlatformAdaptation(
                platform="instagram",
                script="",
                duration_seconds=30,
            )


class TestScriptFramework:
    def test_valid_script(self, sample_script):
        assert sample_script.hook == "Check this out"

    def test_hook_under_20_words(self):
        hook = " ".join(["word"] * 20)
        script = ScriptFramework(
            hook=hook,
            context="Context text",
            demo="Demo text",
            cta="CTA text",
        )
        assert len(script.hook.split()) == 20

    def test_hook_over_20_words_rejected(self):
        # Use short words to stay under max_length=100 but exceed 20 words
        hook = " ".join(["a"] * 21)
        with pytest.raises(ValidationError, match="keep under 20"):
            ScriptFramework(
                hook=hook,
                context="Context text",
                demo="Demo text",
                cta="CTA text",
            )

    def test_hook_max_length_100_chars(self):
        with pytest.raises(ValidationError):
            ScriptFramework(
                hook="x" * 101,
                context="Context",
                demo="Demo",
                cta="CTA",
            )

    def test_cta_max_length_150_chars(self):
        with pytest.raises(ValidationError):
            ScriptFramework(
                hook="Hook",
                context="Context",
                demo="Demo",
                cta="x" * 151,
            )


class TestContentBrief:
    def _make_brief(self, **overrides):
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
            script=ScriptFramework(
                hook="Check this out",
                context="Context here",
                demo="Demo here",
                cta="Try it now",
            ),
            platforms={
                p: PlatformAdaptation(platform=p, script="Script", duration_seconds=30)
                for p in ("instagram", "tiktok", "youtube")
            },
            hashtags=["#feature", "#update"],
        )
        defaults.update(overrides)
        return ContentBrief(**defaults)

    def test_valid_brief(self):
        brief = self._make_brief()
        assert len(brief.platforms) == 3

    def test_missing_platform_rejected(self):
        platforms = {
            p: PlatformAdaptation(platform=p, script="Script", duration_seconds=30)
            for p in ("instagram", "tiktok")
        }
        with pytest.raises(ValidationError, match="Missing platform adaptations"):
            self._make_brief(platforms=platforms)

    def test_missing_all_platforms_rejected(self):
        with pytest.raises(ValidationError, match="Missing platform adaptations"):
            self._make_brief(platforms={})

    def test_invalid_hashtag_format(self):
        with pytest.raises(ValidationError, match="Hashtag must start with #"):
            self._make_brief(hashtags=["#valid", "invalid"])

    def test_all_hashtags_valid(self):
        brief = self._make_brief(hashtags=["#one", "#two", "#three"])
        assert all(t.startswith("#") for t in brief.hashtags)

    def test_empty_hashtags_rejected(self):
        """hashtags field has min_length=1, so empty list is rejected."""
        with pytest.raises(ValidationError):
            self._make_brief(hashtags=[])


class TestContentCalendar:
    def _make_calendar(self, brief_factory, **overrides):
        defaults = dict(
            week_start=date(2025, 3, 3),
            briefs=[brief_factory],
            posting_schedule={},
        )
        defaults.update(overrides)
        return ContentCalendar(**defaults)

    def test_valid_calendar(self, sample_changelog_entry, sample_script, sample_platform_adaptation):
        brief = ContentBrief(
            changelog_entry=sample_changelog_entry,
            headline="Test",
            content_pillar=ContentPillar.FEATURE_DROPS,
            script=sample_script,
            platforms=sample_platform_adaptation,
            hashtags=["#test"],
        )
        cal = ContentCalendar(week_start=date(2025, 3, 3), briefs=[brief])
        assert cal.week_start == date(2025, 3, 3)

    def test_empty_briefs_rejected(self):
        with pytest.raises(ValidationError):
            ContentCalendar(week_start=date(2025, 3, 3), briefs=[])

    def test_duplicate_platform_day_rejected(
        self, sample_changelog_entry, sample_script, sample_platform_adaptation
    ):
        brief = ContentBrief(
            changelog_entry=sample_changelog_entry,
            headline="Test",
            content_pillar=ContentPillar.FEATURE_DROPS,
            script=sample_script,
            platforms=sample_platform_adaptation,
            hashtags=["#test"],
        )
        schedule = {
            "instagram": [
                {"brief_index": 0, "scheduled_date": date(2025, 3, 3)},
                {"brief_index": 1, "scheduled_date": date(2025, 3, 3)},
            ]
        }
        with pytest.raises(ValidationError, match="Duplicate post"):
            ContentCalendar(
                week_start=date(2025, 3, 3),
                briefs=[brief],
                posting_schedule=schedule,
            )

    def test_different_days_allowed(
        self, sample_changelog_entry, sample_script, sample_platform_adaptation
    ):
        brief = ContentBrief(
            changelog_entry=sample_changelog_entry,
            headline="Test",
            content_pillar=ContentPillar.FEATURE_DROPS,
            script=sample_script,
            platforms=sample_platform_adaptation,
            hashtags=["#test"],
        )
        schedule = {
            "instagram": [
                {"brief_index": 0, "scheduled_date": date(2025, 3, 3)},
                {"brief_index": 1, "scheduled_date": date(2025, 3, 4)},
            ]
        }
        cal = ContentCalendar(
            week_start=date(2025, 3, 3),
            briefs=[brief],
            posting_schedule=schedule,
        )
        assert len(cal.posting_schedule["instagram"]) == 2
