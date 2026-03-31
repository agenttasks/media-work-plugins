---
name: slack-workflows
description: |
  Triggers and manages content pipeline workflows from Slack via @Claude mentions.
  Enables team members to request content generation, review experiments,
  and check pipeline status directly from team channels.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: slack
  platform: cloud
---

# Slack Workflows

Mention @Claude in Slack channels to trigger content pipeline workflows. Claude automatically detects coding tasks and routes them to Claude Code on the web.

## Supported Workflows

### Content Generation
```
@Claude Generate content briefs from the latest 3 CHANGELOG entries
for all platforms. Priority: P0.
```

Claude Code on the web:
1. Parses the CHANGELOG
2. Generates ContentBrief models
3. Creates platform adaptations (Instagram, TikTok, YouTube)
4. Posts a summary back to Slack with brief highlights

### Experiment Review
```
@Claude Review experiment EXP-2025-W10 results.
Is the question hook variant winning on TikTok?
```

Claude Code on the web:
1. Reads experiment data
2. Runs statistical analysis
3. Generates a WeeklyReport
4. Posts findings with p-value and recommendation

### Pipeline Status Check
```
@Claude What's the status of today's content pipeline?
How many requirements are pending vs completed?
```

Claude Code on the web:
1. Scans requirements directories
2. Counts by status (pending, accepted, completed, blocked)
3. Reports any blocked items with reasons
4. Posts summary to Slack thread

### Quick Content Review
```
@Claude Review the Instagram adaptation for the dark mode feature brief.
Check hook timing and hashtag compliance.
```

## Slack → Claude Code Routing

| Slack Trigger | Claude Code Action | Plugin |
|---|---|---|
| "generate content" | `/marketing-data-science:generate-content` | marketing-data-science |
| "run experiment" | `/marketing-data-science:run-experiment` | marketing-data-science |
| "generate video" | `/platform-engineering:generate-video` | platform-engineering |
| "upload content" | `/platform-engineering:upload-content` | platform-engineering |
| "dispatch task" | `/media-operations:dispatch-task` | media-operations |
| "schedule" | `/media-operations:schedule-content` | media-operations |

## Context Gathering

Claude gathers context from:
- The Slack thread (conversation history)
- The channel topic (team context)
- Pinned messages (standing instructions)
- The project repository (codebase state)

## Status Updates

Claude posts status updates to the originating Slack thread:
- Task acknowledged (with estimated complexity)
- Progress milestones (briefs generated, videos queued)
- Completion (with links to PRs or artifacts)
- Errors (with suggested resolution)
