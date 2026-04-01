"""Shared fixtures for marketing-data-science tests."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.base import Platform  # noqa: E402
from models.content import (  # noqa: E402
    ChangelogEntry,
    ImpactLevel,
    PlatformAdaptation,
    ScriptFramework,
)
from models.experiments import PlatformMetrics, VariantConfig, VariantResults  # noqa: E402
from models.requirements import ContentSpec, UploadSpec, VideoGenerationSpec  # noqa: E402


@pytest.fixture
def sample_changelog_entry():
    return ChangelogEntry(
        changelog_date=date(2025, 3, 1),
        category="feature",
        title="New dark mode support",
        description="Added dark mode across the entire application.",
        impact_level=ImpactLevel.HIGH,
    )


@pytest.fixture
def sample_script():
    return ScriptFramework(
        hook="Check this out",
        context="We just shipped dark mode for the entire app.",
        demo="Watch how easy it is to toggle between light and dark themes.",
        cta="Try it now and let us know what you think!",
    )


@pytest.fixture
def sample_platform_adaptation():
    return {
        p: PlatformAdaptation(platform=p, script="Sample script content", duration_seconds=30)
        for p in ("instagram", "tiktok", "youtube")
    }


@pytest.fixture
def sample_variant_config():
    return VariantConfig(label="Control", description="Standard hook type", parameters={"hook": "question"})


@pytest.fixture
def sample_platform_metrics():
    return PlatformMetrics(
        platform=Platform.INSTAGRAM,
        views=1000, completions=500, likes=100, comments=50,
        shares=25, new_followers=10, link_clicks=30,
    )


@pytest.fixture
def sample_variant_results(sample_variant_config, sample_platform_metrics):
    return VariantResults(variant=sample_variant_config, platform_metrics=[sample_platform_metrics])


@pytest.fixture
def sample_content_spec():
    return ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=30, script="Demo script for video generation")


@pytest.fixture
def sample_video_generation_spec():
    return VideoGenerationSpec(style="talking_avatar")


@pytest.fixture
def sample_upload_spec():
    return UploadSpec(platform=Platform.TIKTOK, title="New Feature Drop", description="Check out our latest feature.")
