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
    WeeklyReport,
)


class TestPlatformMetrics:
    def test_completion_rate(self, sample_platform_metrics):
        # 500 completions / 1000 views = 0.5
        assert sample_platform_metrics.completion_rate == 0.5

    def test_engagement_rate(self, sample_platform_metrics):
        # (100 likes + 50 comments + 25 shares) / 1000 views = 0.175
        assert sample_platform_metrics.engagement_rate == 0.175

    def test_share_rate(self, sample_platform_metrics):
        # 25 / 1000 = 0.025
        assert sample_platform_metrics.share_rate == 0.025

    def test_follower_conversion(self, sample_platform_metrics):
        # 10 / 1000 = 0.01
        assert sample_platform_metrics.follower_conversion == 0.01

    def test_ctr(self, sample_platform_metrics):
        # 30 / 1000 = 0.03
        assert sample_platform_metrics.ctr == 0.03

    def test_composite_score(self, sample_platform_metrics):
        expected = (
            0.5 * 0.30      # completion_rate
            + 0.175 * 0.25  # engagement_rate
            + 0.025 * 0.20  # share_rate
            + 0.01 * 0.15   # follower_conversion
            + 0.03 * 0.10   # ctr
        )
        assert abs(sample_platform_metrics.composite_score - expected) < 1e-10

    def test_zero_views_all_rates_zero(self):
        metrics = PlatformMetrics(
            platform=Platform.TIKTOK,
            views=0,
            completions=0,
            likes=0,
            comments=0,
            shares=0,
            new_followers=0,
            link_clicks=0,
        )
        assert metrics.completion_rate == 0.0
        assert metrics.engagement_rate == 0.0
        assert metrics.share_rate == 0.0
        assert metrics.follower_conversion == 0.0
        assert metrics.ctr == 0.0
        assert metrics.composite_score == 0.0

    def test_negative_views_rejected(self):
        with pytest.raises(ValidationError):
            PlatformMetrics(
                platform=Platform.INSTAGRAM,
                views=-1,
                completions=0,
                likes=0,
                comments=0,
                shares=0,
                new_followers=0,
                link_clicks=0,
            )


class TestVariantResults:
    def test_total_views(self, sample_variant_results):
        assert sample_variant_results.total_views == 1000

    def test_total_views_multiple_platforms(self, sample_variant_config):
        metrics = [
            PlatformMetrics(
                platform=Platform.INSTAGRAM,
                views=500, completions=0, likes=0, comments=0,
                shares=0, new_followers=0, link_clicks=0,
            ),
            PlatformMetrics(
                platform=Platform.TIKTOK,
                views=300, completions=0, likes=0, comments=0,
                shares=0, new_followers=0, link_clicks=0,
            ),
        ]
        results = VariantResults(variant=sample_variant_config, platform_metrics=metrics)
        assert results.total_views == 800

    def test_avg_composite_score(self, sample_variant_results):
        # Single platform, so avg = that platform's composite score
        assert sample_variant_results.avg_composite_score == pytest.approx(
            sample_variant_results.platform_metrics[0].composite_score
        )

    def test_avg_composite_score_empty(self, sample_variant_config):
        results = VariantResults(variant=sample_variant_config, platform_metrics=[])
        assert results.avg_composite_score == 0.0

    def test_avg_composite_score_filters_zero_views(self, sample_variant_config):
        metrics = [
            PlatformMetrics(
                platform=Platform.INSTAGRAM,
                views=1000, completions=500, likes=100, comments=50,
                shares=25, new_followers=10, link_clicks=30,
            ),
            PlatformMetrics(
                platform=Platform.TIKTOK,
                views=0, completions=0, likes=0, comments=0,
                shares=0, new_followers=0, link_clicks=0,
            ),
        ]
        results = VariantResults(variant=sample_variant_config, platform_metrics=metrics)
        # Only Instagram counted (TikTok has 0 views, filtered out)
        assert results.avg_composite_score == metrics[0].composite_score


class TestExperimentResults:
    def _make_variant_results(self, views: int) -> VariantResults:
        return VariantResults(
            variant=VariantConfig(label="V", description="test"),
            platform_metrics=[
                PlatformMetrics(
                    platform=Platform.INSTAGRAM,
                    views=views, completions=0, likes=0, comments=0,
                    shares=0, new_followers=0, link_clicks=0,
                )
            ],
        )

    def _make_results(self, views_a: int = 200, views_b: int = 200) -> ExperimentResults:
        return ExperimentResults(
            variant_a_results=self._make_variant_results(views_a),
            variant_b_results=self._make_variant_results(views_b),
            statistical_result=StatisticalResult(
                p_value=0.03, effect_size=0.5, significant=True, winner="V"
            ),
            conclusion="Variant A wins",
            recommended_action="Roll out A",
        )

    def test_valid_results(self):
        results = self._make_results(200, 200)
        assert results.variant_a_results.total_views == 200

    def test_variant_a_below_minimum_rejected(self):
        with pytest.raises(ValidationError, match="Variant A has only 199 views"):
            self._make_results(199, 200)

    def test_variant_b_below_minimum_rejected(self):
        with pytest.raises(ValidationError, match="Variant B has only 100 views"):
            self._make_results(200, 100)

    def test_exactly_200_views_accepted(self):
        results = self._make_results(200, 200)
        assert results.variant_a_results.total_views == 200


class TestExperiment:
    def _make_experiment(self, **overrides):
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

    def test_valid_planned_experiment(self):
        exp = self._make_experiment()
        assert exp.status == ExperimentStatus.PLANNED
        assert exp.results is None

    def test_results_without_completed_rejected(self):
        """Results set with non-completed status should raise."""
        results = ExperimentResults(
            variant_a_results=VariantResults(
                variant=VariantConfig(label="A", description="a"),
                platform_metrics=[
                    PlatformMetrics(
                        platform=Platform.INSTAGRAM,
                        views=300, completions=0, likes=0, comments=0,
                        shares=0, new_followers=0, link_clicks=0,
                    )
                ],
            ),
            variant_b_results=VariantResults(
                variant=VariantConfig(label="B", description="b"),
                platform_metrics=[
                    PlatformMetrics(
                        platform=Platform.INSTAGRAM,
                        views=300, completions=0, likes=0, comments=0,
                        shares=0, new_followers=0, link_clicks=0,
                    )
                ],
            ),
            statistical_result=StatisticalResult(
                p_value=0.04, effect_size=0.3, significant=True
            ),
            conclusion="A wins",
            recommended_action="Roll out A",
        )
        with pytest.raises(ValidationError, match="Results can only be set"):
            self._make_experiment(status=ExperimentStatus.RUNNING, results=results)

    def test_completed_without_results_rejected(self):
        with pytest.raises(ValidationError, match="Completed experiments must have results"):
            self._make_experiment(status=ExperimentStatus.COMPLETED, results=None)

    def test_week_number_boundaries(self):
        self._make_experiment(week_number=1)
        self._make_experiment(week_number=53)
        with pytest.raises(ValidationError):
            self._make_experiment(week_number=0)
        with pytest.raises(ValidationError):
            self._make_experiment(week_number=54)

    def test_hypothesis_min_length(self):
        with pytest.raises(ValidationError):
            self._make_experiment(hypothesis="short")

    def test_empty_platforms_rejected(self):
        with pytest.raises(ValidationError):
            self._make_experiment(platforms=[])


class TestStatisticalResult:
    def test_valid_result(self):
        sr = StatisticalResult(
            p_value=0.03, effect_size=0.5, significant=True, winner="Control"
        )
        assert sr.significant is True

    def test_p_value_boundaries(self):
        StatisticalResult(p_value=0.0, effect_size=0.1, significant=False)
        StatisticalResult(p_value=1.0, effect_size=0.1, significant=False)
        with pytest.raises(ValidationError):
            StatisticalResult(p_value=-0.01, effect_size=0.1, significant=False)
        with pytest.raises(ValidationError):
            StatisticalResult(p_value=1.01, effect_size=0.1, significant=False)

    def test_winner_optional(self):
        sr = StatisticalResult(p_value=0.5, effect_size=0.01, significant=False)
        assert sr.winner is None
