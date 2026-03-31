"""Tests for cross-plugin requirements handoff models."""

from __future__ import annotations

from uuid import uuid4

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


class TestContentSpec:
    def test_valid_spec(self, sample_content_spec):
        assert sample_content_spec.resolution == "1080x1920"
        assert sample_content_spec.aspect_ratio == "9:16"

    def test_valid_resolution_formats(self):
        for res in ("1080x1920", "720x1280", "3840x2160"):
            spec = ContentSpec(
                platform=Platform.INSTAGRAM,
                duration_seconds=30,
                script="test",
                resolution=res,
            )
            assert spec.resolution == res

    def test_invalid_resolution_no_x(self):
        with pytest.raises(ValidationError, match="Resolution must be WxH"):
            ContentSpec(
                platform=Platform.INSTAGRAM,
                duration_seconds=30,
                script="test",
                resolution="1080-1920",
            )

    def test_invalid_resolution_non_numeric(self):
        with pytest.raises(ValidationError, match="Resolution must be WxH"):
            ContentSpec(
                platform=Platform.INSTAGRAM,
                duration_seconds=30,
                script="test",
                resolution="widexhigh",
            )

    def test_duration_boundaries(self):
        ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=15, script="test")
        ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=90, script="test")
        with pytest.raises(ValidationError):
            ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=14, script="test")
        with pytest.raises(ValidationError):
            ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=91, script="test")

    def test_empty_script_rejected(self):
        with pytest.raises(ValidationError):
            ContentSpec(platform=Platform.INSTAGRAM, duration_seconds=30, script="")


class TestUploadSpec:
    def test_valid_spec(self, sample_upload_spec):
        assert sample_upload_spec.visibility == "public"

    def test_valid_visibility_values(self):
        for vis in ("public", "private", "unlisted"):
            spec = UploadSpec(
                platform=Platform.YOUTUBE,
                title="Test",
                description="Desc",
                visibility=vis,
            )
            assert spec.visibility == vis

    def test_invalid_visibility_rejected(self):
        with pytest.raises(ValidationError, match="visibility must be one of"):
            UploadSpec(
                platform=Platform.YOUTUBE,
                title="Test",
                description="Desc",
                visibility="draft",
            )

    def test_hashtag_count_at_limit(self):
        tags = [f"#tag{i}" for i in range(30)]
        spec = UploadSpec(
            platform=Platform.INSTAGRAM,
            title="Test",
            description="Desc",
            hashtags=tags,
        )
        assert len(spec.hashtags) == 30

    def test_hashtag_count_over_limit(self):
        tags = [f"#tag{i}" for i in range(31)]
        with pytest.raises(ValidationError, match="Maximum 30 hashtags"):
            UploadSpec(
                platform=Platform.INSTAGRAM,
                title="Test",
                description="Desc",
                hashtags=tags,
            )

    def test_empty_title_rejected(self):
        with pytest.raises(ValidationError):
            UploadSpec(
                platform=Platform.TIKTOK,
                title="",
                description="Desc",
            )

    def test_title_max_length(self):
        with pytest.raises(ValidationError):
            UploadSpec(
                platform=Platform.TIKTOK,
                title="x" * 201,
                description="Desc",
            )

    def test_description_max_length(self):
        with pytest.raises(ValidationError):
            UploadSpec(
                platform=Platform.TIKTOK,
                title="Test",
                description="x" * 5001,
            )


class TestExperimentTracking:
    def test_valid_variants(self):
        for v in ("A", "B"):
            et = ExperimentTracking(variant=v)
            assert et.variant == v

    def test_invalid_variant_rejected(self):
        with pytest.raises(ValidationError):
            ExperimentTracking(variant="C")

    def test_invalid_variant_ab_rejected(self):
        with pytest.raises(ValidationError):
            ExperimentTracking(variant="AB")

    def test_none_variant_allowed(self):
        et = ExperimentTracking()
        assert et.variant is None


class TestRequirement:
    def _make_requirement(self, **overrides):
        defaults = dict(
            source_skill="content-strategy",
            priority=Priority.P1,
            type=RequirementType.INTEGRATION_SETUP,
            acceptance_criteria=["Must integrate with API"],
        )
        defaults.update(overrides)
        return Requirement(**defaults)

    def test_valid_integration_requirement(self):
        req = self._make_requirement()
        assert req.status == RequirementStatus.PENDING

    def test_video_generation_requires_specs(self):
        with pytest.raises(ValidationError, match="VIDEO_GENERATION requirements need"):
            self._make_requirement(type=RequirementType.VIDEO_GENERATION)

    def test_video_generation_requires_both_specs(self, sample_content_spec):
        with pytest.raises(ValidationError, match="VIDEO_GENERATION requirements need"):
            self._make_requirement(
                type=RequirementType.VIDEO_GENERATION,
                content_spec=sample_content_spec,
                # missing video_generation
            )

    def test_video_generation_with_both_specs(
        self, sample_content_spec, sample_video_generation_spec
    ):
        req = self._make_requirement(
            type=RequirementType.VIDEO_GENERATION,
            content_spec=sample_content_spec,
            video_generation=sample_video_generation_spec,
        )
        assert req.type == RequirementType.VIDEO_GENERATION

    def test_content_upload_requires_upload_spec(self):
        with pytest.raises(ValidationError, match="CONTENT_UPLOAD requirements need"):
            self._make_requirement(type=RequirementType.CONTENT_UPLOAD)

    def test_content_upload_with_spec(self, sample_upload_spec):
        req = self._make_requirement(
            type=RequirementType.CONTENT_UPLOAD,
            upload_spec=sample_upload_spec,
        )
        assert req.type == RequirementType.CONTENT_UPLOAD

    def test_blocked_requires_reason(self):
        with pytest.raises(ValidationError, match="Blocked requirements must have"):
            self._make_requirement(status=RequirementStatus.BLOCKED)

    def test_blocked_with_reason(self):
        req = self._make_requirement(
            status=RequirementStatus.BLOCKED,
            blocked_reason="API key expired",
        )
        assert req.blocked_reason == "API key expired"

    def test_rejected_requires_reason(self):
        with pytest.raises(ValidationError, match="Rejected requirements must have"):
            self._make_requirement(status=RequirementStatus.REJECTED)

    def test_rejected_with_reason(self):
        req = self._make_requirement(
            status=RequirementStatus.REJECTED,
            rejected_reason="Out of scope",
        )
        assert req.rejected_reason == "Out of scope"

    def test_empty_acceptance_criteria_rejected(self):
        with pytest.raises(ValidationError):
            self._make_requirement(acceptance_criteria=[])

    def test_measurement_pipeline_no_extra_specs_needed(self):
        req = self._make_requirement(type=RequirementType.MEASUREMENT_PIPELINE)
        assert req.type == RequirementType.MEASUREMENT_PIPELINE
