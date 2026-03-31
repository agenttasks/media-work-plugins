---
name: base-session
description: |
  Base skill providing canonical Claude Code session context for marketing-data-science tasks.
  Inherits session metadata, costs, telemetry, logging, and device surface information.
  All other marketing-data-science skills extend this base context.
user-invocable: false
---

# Base Session Context

This skill provides the foundational session context that all marketing-data-science skills inherit.

## Session Lifecycle Touch Points

### Session Start
- Capture `${CLAUDE_SESSION_ID}` and timestamp
- Detect device surface and user context
- Load environment configuration from `.env.marketing` if present
- Initialize telemetry and cost tracking

### Runtime
- Track token usage and API costs per skill invocation
- Log structured events for content generation, publishing, and measurement
- Maintain session state for multi-step workflows

### Branch Creation
- Auto-create feature branches for content batches: `content/<platform>/<date>`
- Version control all generated content plans and Pydantic model outputs

### Pull Request Events
- Trigger content review workflows on PR creation
- Validate structured outputs against Pydantic schemas
- Run data quality checks before merge

## Telemetry Schema

All skills emit structured telemetry:

```json
{
  "session_id": "${CLAUDE_SESSION_ID}",
  "skill_name": "<invoking-skill>",
  "event_type": "content_generated | experiment_measured | quality_check",
  "platform": "instagram | tiktok | youtube",
  "timestamp": "<ISO-8601>",
  "cost_usd": "<estimated-cost>",
  "tokens_used": "<count>"
}
```

## Logging

- Structured JSON logs to `.claude/logs/marketing-data-science/`
- Log levels: DEBUG, INFO, WARN, ERROR
- Rotate logs per session

## Cost Tracking

- Track per-skill invocation costs
- Aggregate daily/weekly cost reports
- Alert on budget threshold breaches

## Device Surface Detection

At session start, detect:
- Available MCP servers (Higgsfield, social media connectors)
- Local tools (ffmpeg, imagemagick for media processing)
- API keys configured in environment
- Platform engineering plugin availability
