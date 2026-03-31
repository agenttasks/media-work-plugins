---
name: agent-team-coordination
description: |
  Coordinates parallel agent teams for content pipeline tasks.
  A lead session creates tasks and coordinates while teammates work independently
  on research, generation, review, and publishing in parallel.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: agent-teams
  topology: lead-teammate
---

# Agent Team Coordination

Coordinate multiple Claude Code instances working together on content pipeline tasks. One lead session creates tasks and coordinates; teammates work independently and communicate directly.

## Team Topologies

### Content Generation Team
```
Lead: media-operations coordinator
  ├── Researcher: Parse CHANGELOG, identify high-impact entries
  ├── Writer: Generate scripts and platform adaptations
  ├── Reviewer: Validate Pydantic models and quality checks
  └── Publisher: Hand off requirements to platform-engineering
```

### Experiment Analysis Team
```
Lead: media-operations coordinator
  ├── Data Collector: Gather metrics from each platform
  ├── Statistician: Run A/B analysis, compute p-values
  ├── Reporter: Generate WeeklyReport and recommendations
  └── Optimizer: Update content strategy based on findings
```

### Cross-Platform Publishing Team
```
Lead: media-operations coordinator
  ├── Instagram Agent: Adapt, generate, upload Instagram Reels
  ├── TikTok Agent: Adapt, generate, upload TikTok videos
  └── YouTube Agent: Adapt, generate, upload YouTube Shorts
```

## Task Distribution

The lead session:
1. Receives a pipeline task (via dispatch, channel, or schedule)
2. Breaks it into independent subtasks
3. Assigns subtasks to teammate agents
4. Monitors progress via shared task list
5. Synthesizes results when all teammates complete

## Inter-Agent Communication

Teammates communicate through:
- **Shared task list**: Auto-coordination of work items
- **Direct messaging**: Teammates can message each other for context
- **Requirements directory**: Structured handoff via `requirements/` files

## Display Modes

- **In-process**: All agents visible in a single terminal
- **Split panes**: Separate panes in tmux or iTerm2 for parallel monitoring

## When to Use Agent Teams

Use agent teams when:
- Multiple independent content pieces need parallel processing
- Cross-platform publishing can happen simultaneously
- Experiment analysis spans multiple platforms
- Research phase benefits from competing hypotheses

Use a single session when:
- Task is sequential and context-dependent
- Quick one-off content generation
- Simple requirement handoff
