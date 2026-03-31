"""
Version-controlled Pydantic models for marketing-data-science plugin.

Uses structured inputs, inheritance, structured outputs, and data quality checks
for the entire content pipeline from CHANGELOG extraction to social media publishing.
"""

from marketing_data_science.models.base import (
    BaseSessionContext,
    Platform,
    TelemetryEvent,
)
from marketing_data_science.models.content import (
    ChangelogEntry,
    ContentBrief,
    ContentCalendar,
    PlatformAdaptation,
    ScriptFramework,
)
from marketing_data_science.models.experiments import (
    Experiment,
    ExperimentResults,
    ExperimentStatus,
    VariantConfig,
    WeeklyReport,
)
from marketing_data_science.models.requirements import (
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
