---
name: requirements-receiver
description: |
  Receives structured requirements from marketing-data-science plugin.
  Validates, triages, and routes requirements to appropriate integration skills.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Requirements Receiver

Monitors and processes requirements handed off from marketing-data-science.

## Requirement Intake

### Monitor Directory
Watch `media-work-plugins/requirements/pending/` for new requirement files.

### Validation Steps
1. Parse YAML requirement file
2. Validate against Pydantic Requirement model schema
3. Check all required fields for the requirement type
4. Verify referenced resources exist (avatar IDs, platform credentials)

### Triage Logic

| Requirement Type | Route To | Priority Handling |
|-----------------|----------|-------------------|
| `video_generation` | higgsfield-mcp skill | P0: immediate, P1: queue, P2: batch |
| `content_upload` | platform-specific upload skill | P0: immediate, P1: scheduled |
| `integration_setup` | integration-platform skill | Always P1 |
| `measurement_pipeline` | integration-platform skill | P2 unless experiment running |

### Acceptance Flow
```
1. Read requirement from pending/
2. Validate schema and resources
3. Move to accepted/ with timestamp
4. Route to appropriate skill
5. Update status as work progresses
6. Move to completed/ when done
```

## Status Updates

Write status updates back to shared requirements directory:
```yaml
requirement_id: "<uuid>"
status: "accepted | in_progress | completed | blocked"
updated_at: "<ISO-8601>"
notes: "<progress notes>"
blocked_reason: "<if blocked>"
deliverables:
  - path: "<path to generated artifact>"
    type: "video | metadata | analytics_config"
```

## Error Handling

- If requirement validation fails: reject with detailed error
- If platform credentials missing: block with setup instructions
- If Higgsfield API unavailable: block and retry with exponential backoff
- If upload fails: block with platform-specific error details
