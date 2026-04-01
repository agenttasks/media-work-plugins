---
name: dispatch-coordination
description: |
  Coordinates content pipeline tasks via Claude Code's dispatch feature.
  Sends tasks from the Claude mobile app to the Desktop instance, enabling
  delegation of content generation, review, and publishing workflows while away.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: dispatch
  platform: desktop
---

# Dispatch Coordination

Coordinates content pipeline tasks using Claude Code's dispatch capability — send tasks from the Claude mobile app to your local Desktop instance.

## When to Use

- You're away from your desk and want to trigger content generation
- A new CHANGELOG entry needs processing but you're on mobile
- Review a content brief or experiment result remotely
- Kick off a scheduled publish run while commuting

## Dispatch Workflow

### 1. Task Intake (Mobile → Desktop)

From the Claude mobile app, dispatch a task to the running Desktop session:

```
Dispatch: Generate content briefs from the latest CHANGELOG entries
and hand off video generation requirements to platform-engineering
```

The Desktop instance receives the task and begins processing with full local environment access (MCP servers, API keys, file system).

### 2. Pipeline Orchestration

Once dispatched, the task flows through:

```
dispatch received
  → invoke marketing-data-science:generate-content
  → validate Pydantic models
  → write requirements/pending/*.yaml
  → notify platform-engineering via hooks
  → report status back to mobile
```

### 3. Status Reporting

The dispatch coordinator reports progress at key milestones:
- Content briefs generated (count, platforms)
- Requirements handed off (IDs, priority)
- Video generation started (Higgsfield job IDs)
- Upload completed (platform URLs)

## Task Templates

### Content Generation Dispatch
```yaml
task: generate-content
source: dispatch
parameters:
  changelog_range: "latest"
  platforms: [instagram, tiktok, youtube]
  auto_handoff: true
```

### Experiment Review Dispatch
```yaml
task: review-experiment
source: dispatch
parameters:
  experiment_id: "<uuid>"
  action: "analyze_results"
```

### Publish Schedule Dispatch
```yaml
task: schedule-publish
source: dispatch
parameters:
  calendar_week: "current"
  platforms: [instagram, tiktok, youtube]
```
