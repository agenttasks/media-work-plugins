"""Tests for A/B experiment models, metrics, and statistical results."""

from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from models.base import Platform
from models.experiments import (
    Experiment,
    ExperimentResults,
    ExperimentStatus,
    ExperimentVariable,
    PlatformMetrics,
    StatisticalResult,
    VariantConfig,
    VariantResults,
)

ZERO_METRICS = dict(completions=0, likes=0, comments=0, shares=0, new_followers=0, link_clicks=0)


def _metrics(platform=Platform.INSTAGRAM, views=1000, **kw) -> PlatformMetrics:
    return PlatformMetrics(platform=platform, views=views, **{**ZERO_METRICS, **kw})


def _variant_results(views=200, label="V") -> VariantResults:
    return VariantResults(
        variant=VariantConfig(label=label, description="test"),
        platform_metrics=[_metrics(views=views)],
    )


def _experiment_results(views_a=200, views_b=200) -> ExperimentResults:
    return ExperimentResults(
        variant_a_results=_variant_results(views_a, "A"),
        variant_b_results=_variant_results(views_b, "B"),
        statistical_result=StatisticalResult(
            p_value=0.03, effect_size=0.5, significant=True, winner="A"
        ),
        conclusion="Variant A wins",
        recommended_action="Roll out A",
    )


class TestPlatformMetrics:
    def test_rates(self, sample_platform_metrics):
        m = sample_platform_metrics
        assert m.completion_rate == 0.5
        assert m.engagement_rate == 0.175
        assert m.share_rate == 0.025
        assert m.follower_conversion == 0.01
        assert m.ctr == 0.03

    def test_composite_score(self, sample_platform_metrics):
        m = sample_platform_metrics
        expected = (
            m.completion_rate * 0.30
            + m.engagement_rate * 0.25
            + m.share_rate * 0.20
            + m.follower_conversion * 0.15
            + m.ctr * 0.10
        )
        assert abs(m.composite_score - expected) < 1e-10

    def test_zero_views_all_rates_zero(self):
        m = _metrics(views=0)
        assert m.completion_rate == 0.0
        assert m.engagement_rate == 0.0
        assert m.composite_score == 0.0

    def test_negative_views_rejected(self):
        with pytest.raises(ValidationError):
            _metrics(views=-1)


class TestVariantResults:
    def test_total_views(self, sample_variant_results):
        assert sample_variant_results.total_views == 1000

    def test_total_views_multiple_platforms(self, sample_variant_config):
        results = VariantResults(
            variant=sample_variant_config,
            platform_metrics=[_metrics(Platform.INSTAGRAM, 500), _metrics(Platform.TIKTOK, 300)],
        )
        assert results.total_views == 800

    def test_avg_composite_score(self, sample_variant_results):
        assert sample_variant_results.avg_composite_score == pytest.approx(
            sample_variant_results.platform_metrics[0].composite_score
        )

    def test_avg_composite_score_empty(self, sample_variant_config):
        assert VariantResults(variant=sample_variant_config).avg_composite_score == 0.0

    def test_avg_composite_score_filters_zero_views(self, sample_variant_config):
        metrics = [
            _metrics(Platform.INSTAGRAM, 1000, completions=500, likes=100, comments=50,
                     shares=25, new_followers=10, link_clicks=30),
            _metrics(Platform.TIKTOK, 0),
        ]
        results = VariantResults(variant=sample_variant_config, platform_metrics=metrics)
        assert results.avg_composite_score == metrics[0].composite_score


class TestExperimentResults:
    def test_valid_results(self):
        assert _experiment_results().variant_a_results.total_views == 200

    @pytest.mark.parametrize(
        "va,vb,label",
        [(199, 200, "A"), (200, 100, "B")],
    )
    def test_below_minimum_rejected(self, va, vb, label):
        with pytest.raises(ValidationError, match=f"Variant {label} has only"):
            _experiment_results(va, vb)

    def test_exactly_200_views_accepted(self):
        assert _experiment_results(200, 200).variant_a_results.total_views == 200


def _make_experiment(**overrides):
    defaults = dict(
        week_number=10,
        week_start=date(2025, 3, 3),
        hypothesis="Testing whether question hooks increase completion rate",
        variable=ExperimentVariable.HOOK_TYPE,
        variant_a=VariantConfig(label="Control", description="Statement hook"),
        variant_b=VariantConfig(label="Treatment", description="Question hook"),
        platforms=[Platform.INSTAGRAM],
        status=ExperimentStatus.PLANNED,
    )
    defaults.update(overrides)
    return Experiment(**defaults)


class TestExperiment:
    def test_valid_planned_experiment(self):
        exp = _make_experiment()
        assert exp.status == ExperimentStatus.PLANNED
        assert exp.results is None

    def test_results_without_completed_rejected(self):
        with pytest.raises(ValidationError, match="Results can only be set"):
            _make_experiment(status=ExperimentStatus.RUNNING, results=_experiment_results(300, 300))

    def test_completed_without_results_rejected(self):
        with pytest.raises(ValidationError, match="Completed experiments must have results"):
            _make_experiment(status=ExperimentStatus.COMPLETED, results=None)

    @pytest.mark.parametrize("wn,valid", [(0, False), (1, True), (53, True), (54, False)])
    def test_week_number_boundaries(self, wn, valid):
        if valid:
            _make_experiment(week_number=wn)
        else:
            with pytest.raises(ValidationError):
                _make_experiment(week_number=wn)

    def test_hypothesis_min_length(self):
        with pytest.raises(ValidationError):
            _make_experiment(hypothesis="short")

    def test_empty_platforms_rejected(self):
        with pytest.raises(ValidationError):
            _make_experiment(platforms=[])


class TestStatisticalResult:
    def test_valid_result(self):
        sr = StatisticalResult(p_value=0.03, effect_size=0.5, significant=True, winner="Control")
        assert sr.significant is True

    @pytest.mark.parametrize("pv,valid", [(-0.01, False), (0.0, True), (1.0, True), (1.01, False)])
    def test_p_value_boundaries(self, pv, valid):
        if valid:
            StatisticalResult(p_value=pv, effect_size=0.1, significant=False)
        else:
            with pytest.raises(ValidationError):
                StatisticalResult(p_value=pv, effect_size=0.1, significant=False)

    def test_winner_optional(self):
        assert StatisticalResult(p_value=0.5, effect_size=0.01, significant=False).winner is None
