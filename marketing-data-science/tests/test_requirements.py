"""Tests for cross-plugin requirements handoff models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from models.base import Platform
from models.requirements import (
    ContentSpec,
    ExperimentTracking,
    Priority,
    Requirement,
    RequirementStatus,
    RequirementType,
    UploadSpec,
    VideoGenerationSpec,
)


def _content_spec(**kw) -> ContentSpec:
    defaults = dict(platform=Platform.INSTAGRAM, duration_seconds=30, script="test")
    defaults.update(kw)
    return ContentSpec(**defaults)


def _upload_spec(**kw) -> UploadSpec:
    defaults = dict(platform=Platform.TIKTOK, title="Test", description="Desc")
    defaults.update(kw)
    return UploadSpec(**defaults)


def _requirement(**overrides) -> Requirement:
    defaults = dict(
        source_skill="content-strategy",
        priority=Priority.P1,
        type=RequirementType.INTEGRATION_SETUP,
        acceptance_criteria=["Must integrate with API"],
    )
    defaults.update(overrides)
    return Requirement(**defaults)


class TestContentSpec:
    def test_valid_spec(self, sample_content_spec):
        assert sample_content_spec.resolution == "1080x1920"
        assert sample_content_spec.aspect_ratio == "9:16"

    @pytest.mark.parametrize("res", ["1080x1920", "720x1280", "3840x2160"])
    def test_valid_resolution_formats(self, res):
        assert _content_spec(resolution=res).resolution == res

    @pytest.mark.parametrize("res", ["1080-1920", "widexhigh"])
    def test_invalid_resolution_rejected(self, res):
        with pytest.raises(ValidationError, match="Resolution must be WxH"):
            _content_spec(resolution=res)

    @pytest.mark.parametrize("dur,valid", [(14, False), (15, True), (90, True), (91, False)])
    def test_duration_boundaries(self, dur, valid):
        if valid:
            _content_spec(duration_seconds=dur)
        else:
            with pytest.raises(ValidationError):
                _content_spec(duration_seconds=dur)

    def test_empty_script_rejected(self):
        with pytest.raises(ValidationError):
            ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=30, script="")


class TestUploadSpec:
    def test_valid_spec(self, sample_upload_spec):
        assert sample_upload_spec.visibility == "public"

    @pytest.mark.parametrize("vis", ["public", "private", "unlisted"])
    def test_valid_visibility_values(self, vis):
        assert _upload_spec(visibility=vis).visibility == vis

    def test_invalid_visibility_rejected(self):
        with pytest.raises(ValidationError):
            _upload_spec(visibility="draft")

    def test_hashtag_count_at_limit(self):
        assert len(_upload_spec(hashtags=[f"#tag{i}" for i in range(30)]).hashtags) == 30

    def test_hashtag_count_over_limit(self):
        with pytest.raises(ValidationError):
            _upload_spec(hashtags=[f"#tag{i}" for i in range(31)])

    def test_empty_title_rejected(self):
        with pytest.raises(ValidationError):
            _upload_spec(title="")

    @pytest.mark.parametrize(
        "field,length", [("title", 201), ("description", 5001)]
    )
    def test_field_max_length(self, field, length):
        with pytest.raises(ValidationError):
            _upload_spec(**{field: "x" * length})


class TestExperimentTracking:
    @pytest.mark.parametrize("v", ["A", "B"])
    def test_valid_variants(self, v):
        assert ExperimentTracking(variant=v).variant == v

    @pytest.mark.parametrize("v", ["C", "AB"])
    def test_invalid_variant_rejected(self, v):
        with pytest.raises(ValidationError):
            ExperimentTracking(variant=v)

    def test_none_variant_allowed(self):
        assert ExperimentTracking().variant is None


class TestRequirement:
    def test_valid_integration_requirement(self):
        assert _requirement().status == RequirementStatus.PENDING

    def test_video_generation_requires_specs(self):
        with pytest.raises(ValidationError, match="VIDEO_GENERATION requirements need"):
            _requirement(type=RequirementType.VIDEO_GENERATION)

    def test_video_generation_requires_both_specs(self, sample_content_spec):
        with pytest.raises(ValidationError, match="VIDEO_GENERATION requirements need"):
            _requirement(type=RequirementType.VIDEO_GENERATION, content_spec=sample_content_spec)

    def test_video_generation_with_both_specs(
        self, sample_content_spec, sample_video_generation_spec
    ):
        req = _requirement(
            type=RequirementType.VIDEO_GENERATION,
            content_spec=sample_content_spec,
            video_generation=sample_video_generation_spec,
        )
        assert req.type == RequirementType.VIDEO_GENERATION

    def test_content_upload_requires_upload_spec(self):
        with pytest.raises(ValidationError, match="CONTENT_UPLOAD requirements need"):
            _requirement(type=RequirementType.CONTENT_UPLOAD)

    def test_content_upload_with_spec(self, sample_upload_spec):
        req = _requirement(type=RequirementType.CONTENT_UPLOAD, upload_spec=sample_upload_spec)
        assert req.type == RequirementType.CONTENT_UPLOAD

    @pytest.mark.parametrize(
        "status,reason_field",
        [
            (RequirementStatus.BLOCKED, "blocked_reason"),
            (RequirementStatus.REJECTED, "rejected_reason"),
        ],
    )
    def test_status_requires_reason(self, status, reason_field):
        with pytest.raises(ValidationError):
            _requirement(status=status)

    @pytest.mark.parametrize(
        "status,reason_field,reason",
        [
            (RequirementStatus.BLOCKED, "blocked_reason", "API key expired"),
            (RequirementStatus.REJECTED, "rejected_reason", "Out of scope"),
        ],
    )
    def test_status_with_reason(self, status, reason_field, reason):
        req = _requirement(status=status, **{reason_field: reason})
        assert getattr(req, reason_field) == reason

    def test_empty_acceptance_criteria_rejected(self):
        with pytest.raises(ValidationError):
            _requirement(acceptance_criteria=[])

    def test_measurement_pipeline_no_extra_specs_needed(self):
        assert _requirement(type=RequirementType.MEASUREMENT_PIPELINE).type == RequirementType.MEASUREMENT_PIPELINE
