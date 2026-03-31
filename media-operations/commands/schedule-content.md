# Schedule recurring content generation and publishing

Set up scheduled automation for the content pipeline using Claude Code's scheduled tasks.

## Usage

```
/media-operations:schedule-content [schedule-type] [--cron <expression>] [--scope <cli|desktop|cloud>]
```

## Schedule Types

- `daily-pipeline` - Daily CHANGELOG parsing and brief generation
- `platform-publish` - Platform-specific publishing windows
- `weekly-report` - Weekly experiment analysis and reporting
- `health-check` - Recurring CI/CD validation

## Examples

```
/media-operations:schedule-content daily-pipeline --cron "0 8 * * *" --scope cloud
/media-operations:schedule-content platform-publish --platform tiktok --cron "0 18 * * 2,4"
/media-operations:schedule-content weekly-report --scope cloud
/media-operations:schedule-content health-check --scope cli
```

## Quick Polling

For session-scoped polling, use `/loop` directly:
```
/loop 5m Check for new requirements and process any pending handoffs
```
