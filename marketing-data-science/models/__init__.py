"""
Version-controlled Pydantic models for marketing-data-science plugin.

Uses structured inputs, inheritance, structured outputs, and data quality checks
for the entire content pipeline from CHANGELOG extraction to social media publishing.
"""

from .base import (
    BaseSessionContext,
    Platform,
    TelemetryEvent,
)
from .content import (
    ChangelogEntry,
    ContentBrief,
    ContentCalendar,
    PlatformAdaptation,
    ScriptFramework,
)
from .experiments import (
    Experiment,
    ExperimentResults,
    ExperimentStatus,
    VariantConfig,
    WeeklyReport,
)
from .requirements import (
    ContentSpec,
    Requirement,
    RequirementStatus,
    RequirementType,
    UploadSpec,
    VideoGenerationSpec,
)

__all__ = [
    "BaseSessionContext",
    "Platform",
    "TelemetryEvent",
    "ChangelogEntry",
    "ContentBrief",
    "ContentCalendar",
    "PlatformAdaptation",
    "ScriptFramework",
    "Experiment",
    "ExperimentResults",
    "ExperimentStatus",
    "VariantConfig",
    "WeeklyReport",
    "ContentSpec",
    "Requirement",
    "RequirementStatus",
    "RequirementType",
    "UploadSpec",
    "VideoGenerationSpec",
]
