---
name: cowork-orchestration
description: |
  Orchestrates multi-plugin coordination using Claude Code's cowork patterns.
  Manages the handoff between marketing-data-science, media-operations,
  and platform-engineering as a unified content pipeline.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: cowork
  plugins: marketing-data-science,platform-engineering,media-operations
---

# Cowork Orchestration

Coordinates the three media-work-plugins as a unified pipeline using Claude Code's cowork create/connect patterns.

## Plugin Topology

```
┌─────────────────────────┐
│  marketing-data-science  │  Content strategy, experiments, briefs
│  (knowledge worker)      │
└──────────┬──────────────┘
           │ requirements/pending/
┌──────────▼──────────────┐
│  media-operations        │  Orchestration, dispatch, scheduling
│  (coordinator)           │
└──────────┬──────────────┘
           │ agent teams, channels
┌──────────▼──────────────┐
│  platform-engineering    │  Video gen, uploads, integrations
│  (executor)              │
└─────────────────────────┘
```

## Cowork Patterns

### Create Pattern
Initialize a new content pipeline session:
1. Start marketing-data-science session (content strategy)
2. Start platform-engineering session (execution readiness)
3. Media-operations coordinates via shared requirements directory

### Connect Pattern
Connect to existing sessions for ongoing coordination:
1. Resume marketing-data-science context (experiment state)
2. Resume platform-engineering context (Higgsfield jobs)
3. Synchronize requirement statuses across plugins

## Pipeline Stages

### Stage 1: Content Generation
- marketing-data-science parses CHANGELOG
- Generates ContentBrief with platform adaptations
- Validates against Pydantic schemas

### Stage 2: Requirement Handoff
- media-operations validates and dispatches requirements
- Routes to appropriate agent teams
- Tracks handoff telemetry

### Stage 3: Execution
- platform-engineering receives requirements
- Generates video via Higgsfield MCP
- Uploads to target platforms

### Stage 4: Measurement
- marketing-data-science collects experiment data
- Runs A/B analysis
- Generates weekly reports

## Coordination Rules

- Only one content pipeline run per platform per day
- Experiment variants must not overlap scheduling windows
- Failed requirements retry up to 3 times before escalating
- All cross-plugin communication goes through `requirements/` directory
