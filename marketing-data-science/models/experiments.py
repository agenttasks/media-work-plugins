"""Pydantic models for A/B experiment design, tracking, and reporting."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from .base import Platform


class ExperimentStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ExperimentVariable(str, Enum):
    HOOK_TYPE = "hook_type"
    DURATION = "duration"
    STYLE = "style"
    POSTING_TIME = "posting_time"
    CTA_TYPE = "cta_type"
    AUDIO = "audio"


class VariantConfig(BaseModel):
    """Configuration for a single experiment variant."""

    label: str = Field(min_length=1, max_length=50)
    description: str
    parameters: dict[str, str | int | float | bool] = Field(default_factory=dict)


class PlatformMetrics(BaseModel):
    """Metrics collected from a single platform for one variant."""

    platform: Platform
    views: int = Field(ge=0)
    completions: int = Field(ge=0)
    likes: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    new_followers: int = Field(ge=0)
    link_clicks: int = Field(ge=0)

    @property
    def completion_rate(self) -> float:
        return self.completions / self.views if self.views > 0 else 0.0

    @property
    def engagement_rate(self) -> float:
        if self.views == 0:
            return 0.0
        return (self.likes + self.comments + self.shares) / self.views

    @property
    def share_rate(self) -> float:
        return self.shares / self.views if self.views > 0 else 0.0

    @property
    def follower_conversion(self) -> float:
        return self.new_followers / self.views if self.views > 0 else 0.0

    @property
    def ctr(self) -> float:
        return self.link_clicks / self.views if self.views > 0 else 0.0

    @property
    def composite_score(self) -> float:
        """Weighted composite score."""
        return (
            self.completion_rate * 0.30
            + self.engagement_rate * 0.25
            + self.share_rate * 0.20
            + self.follower_conversion * 0.15
            + self.ctr * 0.10
        )


class VariantResults(BaseModel):
    """Aggregated results for one variant across platforms."""

    variant: VariantConfig
    platform_metrics: list[PlatformMetrics] = Field(default_factory=list)

    @property
    def total_views(self) -> int:
        return sum(m.views for m in self.platform_metrics)

    @property
    def avg_composite_score(self) -> float:
        scores = [m.composite_score for m in self.platform_metrics if m.views > 0]
        return sum(scores) / len(scores) if scores else 0.0


class StatisticalResult(BaseModel):
    """Statistical comparison between two variants."""

    p_value: float = Field(ge=0.0, le=1.0)
    effect_size: float = Field(description="Cohen's h")
    significant: bool = Field(description="p < 0.05")
    confidence_level: float = Field(default=0.95)
    winner: str | None = Field(
        default=None, description="Label of winning variant, or None if inconclusive"
    )


class ExperimentResults(BaseModel):
    """Complete results for a finished experiment."""

    variant_a_results: VariantResults
    variant_b_results: VariantResults
    statistical_result: StatisticalResult
    conclusion: str
    recommended_action: str
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_minimum_sample(self) -> ExperimentResults:
        """Warn if sample size is below minimum for statistical significance."""
        min_views = 200
        if self.variant_a_results.total_views < min_views:
            raise ValueError(
                f"Variant A has only {self.variant_a_results.total_views} views; "
                f"minimum {min_views} required for significance"
            )
        if self.variant_b_results.total_views < min_views:
            raise ValueError(
                f"Variant B has only {self.variant_b_results.total_views} views; "
                f"minimum {min_views} required for significance"
            )
        return self


class Experiment(BaseModel):
    """A single A/B experiment with weekly cadence."""

    experiment_id: UUID = Field(default_factory=uuid4)
    week_number: int = Field(ge=1, le=53, description="ISO week number")
    week_start: date
    hypothesis: str = Field(min_length=10)
    variable: ExperimentVariable
    variant_a: VariantConfig = Field(description="Control variant")
    variant_b: VariantConfig = Field(description="Treatment variant")
    platforms: list[Platform] = Field(min_length=1)
    status: ExperimentStatus = Field(default=ExperimentStatus.PLANNED)
    results: ExperimentResults | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_results_status(self) -> Experiment:
        if self.results is not None and self.status != ExperimentStatus.COMPLETED:
            raise ValueError("Results can only be set when status is 'completed'")
        if self.status == ExperimentStatus.COMPLETED and self.results is None:
            raise ValueError("Completed experiments must have results")
        return self


class WeeklyReport(BaseModel):
    """Weekly experiment report."""

    experiment: Experiment
    report_date: date
    summary: str
    next_experiment_hypothesis: str | None = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
