# Connectors - Marketing Data Science

## Required Connectors

This plugin does not directly connect to external services. It generates structured requirements
that are fulfilled by the **platform-engineering** plugin.

## Cross-Plugin Communication

| Direction | Channel | Format |
|-----------|---------|--------|
| marketing-data-science → platform-engineering | `requirements/pending/` | YAML (Requirement model) |
| platform-engineering → marketing-data-science | `requirements/completed/` | YAML (status update) |

## Optional Integrations

- **GitHub API**: For fetching `anthropics/claude-code/CHANGELOG.md` (via `curl` in changelog-content skill)
- **Analytics dashboards**: For importing experiment results (manual or CSV)
