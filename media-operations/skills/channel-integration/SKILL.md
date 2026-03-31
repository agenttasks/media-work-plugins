---
name: channel-integration
description: |
  Integrates external event channels (Telegram, Discord, webhooks) into Claude Code sessions.
  Reacts to CI/CD failures, content review requests, and platform notifications
  to trigger automated pipeline responses.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: channels
  platforms: telegram,discord,webhook
---

# Channel Integration

Push events from chat apps (Telegram, Discord) or custom webhook servers into running Claude Code sessions. Claude reacts to these events in real-time for content pipeline automation.

## Supported Channels

### Telegram
- Content review requests from team members
- Publishing approval/rejection notifications
- Experiment result alerts

### Discord
- CI/CD failure notifications triggering auto-fix workflows
- Content calendar updates
- Cross-team coordination messages

### Custom Webhooks
- Platform API notifications (upload complete, analytics ready)
- Higgsfield job completion callbacks
- Social media engagement threshold alerts

## Event Handling

### CI/CD Failure Response
When a channel pushes a CI failure event:
1. Parse the failure context (test name, error message)
2. Invoke the relevant fix workflow
3. Run validation (`scripts/validate.sh`)
4. Report resolution status back to channel

### Content Review Flow
When a review request arrives via channel:
1. Read the content brief from `requirements/pending/`
2. Validate against Pydantic schemas
3. Run quality checks (hook word count, platform requirements)
4. Post approval/feedback to the originating channel

### Platform Notification Flow
When a platform sends a completion webhook:
1. Update requirement status in `requirements/completed/`
2. Trigger measurement pipeline if experiment tracking is active
3. Notify marketing-data-science via PostToolUse hook

## Channel Configuration

Configure channels in `.claude/settings.json`:
```json
{
  "channels": {
    "telegram": {
      "allowedSenders": ["@content-team"],
      "autoReact": true
    },
    "discord": {
      "guild": "media-ops",
      "channels": ["#ci-alerts", "#content-review"]
    }
  }
}
```

## Security

- Sender allowlists prevent unauthorized access
- Channel events are logged to telemetry
- Sensitive operations require explicit approval
