---
name: scheduled-automation
description: |
  Manages recurring content generation, publishing, and reporting tasks
  using Claude Code's scheduled tasks and /loop capabilities.
  Supports CLI, Desktop, and cloud scheduling scopes.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: scheduled-tasks
  scopes: cli,desktop,cloud
---

# Scheduled Automation

Run content pipeline tasks automatically on a schedule using Claude Code's scheduled tasks (`/loop`, Desktop scheduling, and cloud triggers).

## Scheduling Scopes

### CLI Session (`/loop`)
Quick polling within a running session:
```
/loop 5m Check for new CHANGELOG entries and generate content briefs if found
```

### Desktop (Durable)
Persists across sessions on your local machine:
- Daily content generation at 8am
- Hourly requirement status checks
- Weekly experiment report generation

### Cloud (Unattended)
Runs on Anthropic infrastructure without your machine:
- Daily CHANGELOG parsing and brief generation
- Scheduled social media publishing
- Weekly A/B experiment analysis

## Scheduled Pipelines

### Daily Content Pipeline (8:00 AM UTC)
```yaml
schedule: "0 8 * * *"
scope: cloud
tasks:
  - Parse CHANGELOG for new entries since last run
  - Generate ContentBrief for each new entry
  - Create platform adaptations (Instagram, TikTok, YouTube)
  - Write requirements to pending/
  - Trigger platform-engineering handoff
```

### Content Publishing (configurable per platform)
```yaml
schedules:
  instagram:
    cron: "0 12 * * 1,3,5"  # Mon/Wed/Fri at noon
    action: Upload queued Instagram content
  tiktok:
    cron: "0 18 * * 2,4"    # Tue/Thu at 6pm
    action: Upload queued TikTok content
  youtube:
    cron: "0 10 * * 6"      # Saturday at 10am
    action: Upload queued YouTube Shorts
```

### Weekly Report (Friday 5:00 PM UTC)
```yaml
schedule: "0 17 * * 5"
scope: cloud
tasks:
  - Collect experiment metrics from all platforms
  - Run statistical analysis on active experiments
  - Generate WeeklyReport model
  - Post summary to Slack
```

### CI/CD Health Check (`/loop`)
```
/loop 5m Run scripts/validate.sh and report any failures
```

Monitors:
- Skill validation (skills-ref)
- Type checking (mypy)
- Linting (ruff)
- Test suite (pytest)

## Retry and Failure Handling

- Failed scheduled tasks retry up to 3 times with exponential backoff
- Persistent failures are reported to the configured notification channel
- Each run logs cost, duration, and outcome to telemetry
