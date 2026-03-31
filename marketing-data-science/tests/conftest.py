"""Shared fixtures for marketing-data-science tests."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

# Add the parent directory so we can import the models package directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.base import DeviceSurface, Platform  # noqa: E402
from models.content import (  # noqa: E402
    ChangelogEntry,
    ContentPillar,
    ImpactLevel,
    PlatformAdaptation,
    ScriptFramework,
)
from models.experiments import (  # noqa: E402
    ExperimentStatus,
    ExperimentVariable,
    PlatformMetrics,
    StatisticalResult,
    VariantConfig,
    VariantResults,
)
from models.requirements import (  # noqa: E402
    ContentSpec,
    ExperimentTracking,
    Priority,
    RequirementStatus,
    RequirementType,
    UploadSpec,
    VideoGenerationSpec,
)


@pytest.fixture
def sample_changelog_entry() -> ChangelogEntry:
    return ChangelogEntry(
        changelog_date=date(2025, 3, 1),
        category="feature",
        title="New dark mode support",
        description="Added dark mode across the entire application.",
        impact_level=ImpactLevel.HIGH,
    )


@pytest.fixture
def sample_script() -> ScriptFramework:
    return ScriptFramework(
        hook="Check this out",
        context="We just shipped dark mode for the entire app.",
        demo="Watch how easy it is to toggle between light and dark themes.",
        cta="Try it now and let us know what you think!",
    )


@pytest.fixture
def sample_platform_adaptation() -> dict[str, PlatformAdaptation]:
    platforms = {}
    for p in ["instagram", "tiktok", "youtube"]:
        platforms[p] = PlatformAdaptation(
            platform=p,
            script="Sample script content",
            duration_seconds=30,
        )
    return platforms


@pytest.fixture
def sample_variant_config() -> VariantConfig:
    return VariantConfig(
        label="Control",
        description="Standard hook type",
        parameters={"hook": "question"},
    )


@pytest.fixture
def sample_platform_metrics() -> PlatformMetrics:
    return PlatformMetrics(
        platform=Platform.INSTAGRAM,
        views=1000,
        completions=500,
        likes=100,
        comments=50,
        shares=25,
        new_followers=10,
        link_clicks=30,
    )


@pytest.fixture
def sample_variant_results(sample_variant_config, sample_platform_metrics) -> VariantResults:
    return VariantResults(
        variant=sample_variant_config,
        platform_metrics=[sample_platform_metrics],
    )


@pytest.fixture
def sample_content_spec() -> ContentSpec:
    return ContentSpec(
        platform=Platform.INSTAGRAM,
        duration_seconds=30,
        script="Demo script for video generation",
    )


@pytest.fixture
def sample_video_generation_spec() -> VideoGenerationSpec:
    return VideoGenerationSpec(style="talking_avatar")


@pytest.fixture
def sample_upload_spec() -> UploadSpec:
    return UploadSpec(
        platform=Platform.TIKTOK,
        title="New Feature Drop",
        description="Check out our latest feature.",
        visibility="public",
    )
