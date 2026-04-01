# media-operations

Orchestration plugin for autonomous media content pipeline management using Claude Code's latest capabilities.

## Overview

media-operations bridges marketing-data-science and platform-engineering by leveraging Claude Code's dispatch, channels, cowork, remote control, Slack, and scheduled task features for hands-off content pipeline automation.

## Skills

| Skill | Description |
|-------|-------------|
| `dispatch-coordination` | Send tasks from mobile to Desktop via Claude dispatch |
| `channel-integration` | Push events from Telegram, Discord, or custom webhooks into sessions |
| `cowork-orchestration` | Multi-plugin coordination using cowork create/connect patterns |
| `remote-control-ops` | Drive running sessions from claude.ai/code or mobile app |
| `slack-workflows` | Trigger content pipelines from Slack @Claude mentions |
| `scheduled-automation` | Recurring content generation, publishing, and reporting via /loop and cron |
| `agent-team-coordination` | Parallel agent teams for research, generation, and review |

## Commands

| Command | Description |
|---------|-------------|
| `/media-operations:dispatch-task` | Dispatch a content pipeline task to agent teams |
| `/media-operations:schedule-content` | Schedule recurring content generation and publishing |

## Subagents

The plugin ships with skill-creator subagents for planning and building new skills:

| Subagent | Purpose |
|----------|---------|
| `skill-creator-cli` | CLI tool planning for new skills |
| `skill-creator-task` | Task decomposition and planning |
| `skill-creator-prompt` | Prompt engineering for skill system prompts |
| `skill-creator-eval` | Evaluation framework for skill quality |
| `skill-creator-skill` | Skill structure and frontmatter planning |
| `skill-creator-context` | Context management and memory planning |
| `skill-creator-agent-teams` | Agent team topology planning |
| `skill-creator-telemetry` | Telemetry, cost, and usage tracking |
| `skill-creator-docs` | Documentation generation via Mintlify |

## Architecture

```
marketing-data-science (content strategy)
        ↓ requirements/pending/
media-operations (orchestration & dispatch)
        ↓ agent teams, channels, scheduled tasks
platform-engineering (video gen & upload)
        ↓ requirements/completed/
marketing-data-science (measurement & iteration)
```
