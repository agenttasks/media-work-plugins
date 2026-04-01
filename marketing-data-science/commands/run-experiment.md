---
name: run-experiment
description: |
  Create and manage A/B experiments for social media content optimization.
  Design experiments, deploy variants, and analyze results with statistical rigor.
allowed-tools: Read, Write, Bash, Grep
---

# Run A/B Experiment

1. Use the `ab-experiment-measurement` skill to design the experiment
2. Validate experiment design against Pydantic Experiment model
3. Deploy variants according to weekly schedule
4. Collect metrics from platform analytics
5. Analyze results with statistical significance testing
6. Generate weekly report

Arguments:
- `$1`: Action - `create`, `status`, `analyze`, `report`
- `$2`: Experiment ID (for status/analyze/report) or variable name (for create)
