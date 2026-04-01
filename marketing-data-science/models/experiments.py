"""Pydantic models for A/B experiment design, tracking, and reporting."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from .base import NonNegativeInt, Platform

MIN_SAMPLE_VIEWS = 200


class ExperimentStatus(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ExperimentVariable(StrEnum):
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
    views: NonNegativeInt
    completions: NonNegativeInt
    likes: NonNegativeInt
    comments: NonNegativeInt
    shares: NonNegativeInt
    new_followers: NonNegativeInt
    link_clicks: NonNegativeInt

    def _rate(self, numerator: int) -> float:
        return numerator / self.views if self.views > 0 else 0.0

    @property
    def completion_rate(self) -> float:
        return self._rate(self.completions)

    @property
    def engagement_rate(self) -> float:
        return self._rate(self.likes + self.comments + self.shares)

    @property
    def share_rate(self) -> float:
        return self._rate(self.shares)

    @property
    def follower_conversion(self) -> float:
        return self._rate(self.new_followers)

    @property
    def ctr(self) -> float:
        return self._rate(self.link_clicks)

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


ConfidenceLevel = Annotated[float, Field(ge=0.0, le=1.0)]


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

    p_value: ConfidenceLevel
    effect_size: float
    significant: bool
    confidence_level: ConfidenceLevel = 0.95
    winner: str | None = None


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
        for label, variant in [("A", self.variant_a_results), ("B", self.variant_b_results)]:
            if variant.total_views < MIN_SAMPLE_VIEWS:
                raise ValueError(
                    f"Variant {label} has only {variant.total_views} views; "
                    f"minimum {MIN_SAMPLE_VIEWS} required for significance"
                )
        return self


class Experiment(BaseModel):
    """A single A/B experiment with weekly cadence."""

    experiment_id: UUID = Field(default_factory=uuid4)
    week_number: int = Field(ge=1, le=53)
    week_start: date
    hypothesis: str = Field(min_length=10)
    variable: ExperimentVariable
    variant_a: VariantConfig
    variant_b: VariantConfig
    platforms: list[Platform] = Field(min_length=1)
    status: ExperimentStatus = ExperimentStatus.PLANNED
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
