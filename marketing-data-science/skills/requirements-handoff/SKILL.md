---
name: requirements-handoff
description: |
  Generates structured requirements from marketing-data-science and hands them off
  to platform-engineering as actionable tasks. Bridges content strategy with technical execution.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Requirements Handoff to Platform Engineering

This skill bridges marketing-data-science decisions into actionable platform-engineering tasks.

## Requirement Structure

Every handoff produces a structured requirement document:

```yaml
requirement_id: "REQ-<date>-<sequence>"
source_skill: "<originating-skill>"
priority: "P0 | P1 | P2"
type: "video_generation | content_upload | integration_setup | measurement_pipeline"

content_spec:
  platform: "tiktok | instagram | youtube"
  duration_seconds: <int>
  aspect_ratio: "9:16"
  resolution: "1080x1920"
  script: "<full script text>"
  visual_style: "<style description>"
  audio: "<audio specification>"

video_generation:
  provider: "higgsfield"
  model: "<model-name>"
  parameters:
    style: "<generation style>"
    avatar: "<avatar-id or null>"
    lip_sync: <boolean>
    camera_controls: "<camera motion>"

upload_spec:
  platform: "<target platform>"
  title: "<title>"
  description: "<description>"
  hashtags: ["<tag1>", "<tag2>"]
  scheduled_time: "<ISO-8601>"
  visibility: "public | private | unlisted"

experiment:
  experiment_id: "<uuid or null>"
  variant: "A | B | null"
  tracking_params: {}

acceptance_criteria:
  - "<criterion 1>"
  - "<criterion 2>"
```

## Handoff Process

1. **Validate** - Ensure all required fields are populated
2. **Write** - Save requirement to `requirements/pending/<requirement_id>.yaml`
3. **Notify** - Log handoff event to telemetry
4. **Track** - Mark requirement as `pending` in requirements tracker

## Requirement Types

### Video Generation Request
- Sent when content-strategy produces a finalized brief
- Platform-engineering uses Higgsfield MCP to generate

### Content Upload Request
- Sent when video is ready for publishing
- Platform-engineering handles platform-specific upload APIs

### Integration Setup Request
- Sent when research-account-setup identifies new platform needs
- Platform-engineering configures MCP servers and API connections

### Measurement Pipeline Request
- Sent when ab-experiment-measurement needs analytics data
- Platform-engineering configures data collection from platform APIs

## Status Tracking

Requirements flow through states:
```
pending → accepted → in_progress → completed → verified
                  → blocked (with reason)
                  → rejected (with reason)
```

## Cross-Plugin Communication

Requirements are written to a shared directory that platform-engineering monitors:
- `media-work-plugins/requirements/pending/` - New requirements
- `media-work-plugins/requirements/accepted/` - Acknowledged by platform-engineering
- `media-work-plugins/requirements/completed/` - Delivered by platform-engineering
