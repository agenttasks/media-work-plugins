# Marketing Data Science Plugin

Content strategy and data science plugin for creating daily social media shorts from the
[Anthropic Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).

## Skills

| Skill | Description |
|-------|-------------|
| `base-session` | Base session context with telemetry, costs, logging, device surface detection |
| `changelog-content` | Parses CHANGELOG.md and generates content briefs |
| `content-strategy` | Multi-platform content strategy for Instagram, TikTok, YouTube Shorts |
| `cold-start-strategy` | 30-day cold start plan for launching from zero |
| `ab-experiment-measurement` | Week-based A/B experiment framework with statistical analysis |
| `research-account-setup` | Platform account and API setup guide |
| `requirements-handoff` | Structured requirements handoff to platform-engineering |

## Commands

| Command | Description |
|---------|-------------|
| `/marketing-data-science:generate-content` | Generate content briefs from CHANGELOG |
| `/marketing-data-science:run-experiment` | Create and manage A/B experiments |

## Pydantic Models

Version-controlled models in `models/` provide:
- **Structured inputs**: Validated CHANGELOG entries, experiment configs
- **Inheritance**: All models extend `BaseSessionContext` for telemetry
- **Structured outputs**: ContentBrief, WeeklyReport, Requirement
- **Data quality checks**: Field validators, model validators, cross-field consistency

## Content Pipeline

```
CHANGELOG.md → changelog-content → content-strategy → requirements-handoff → platform-engineering
                                         ↓
                                  cold-start-strategy (phase adjustment)
                                         ↓
                                  ab-experiment-measurement (variant tracking)
```

## Installation

```bash
claude plugin marketplace add agenttasks/media-work-plugins
claude plugin install marketing-data-science@media-work-plugins
```
