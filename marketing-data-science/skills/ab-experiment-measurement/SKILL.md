---
name: ab-experiment-measurement
description: |
  Week-based A/B experiment measurement framework for social media content.
  Tracks variants, measures performance, and provides statistical analysis for content optimization.
allowed-tools: Read, Write, Bash, Grep
---

# A/B Experiment Measurement

Week-based experimentation framework for optimizing social media content performance.

## Experiment Design

### Variant Definition
Each experiment tests exactly ONE variable:
- **Hook type**: Question vs statement vs demo-first
- **Duration**: 15s vs 30s vs 45s vs 60s
- **Style**: Avatar vs screen recording vs text overlay
- **Posting time**: Morning vs midday vs evening
- **CTA type**: Follow vs try-it vs comment
- **Audio**: Trending sound vs original vs voiceover only

### Weekly Experiment Structure
```
Monday:    Deploy Variant A on all platforms
Tuesday:   Deploy Variant B on all platforms
Wednesday: Deploy Variant A (replication)
Thursday:  Deploy Variant B (replication)
Friday:    Collect and analyze results
Saturday:  Generate report and plan next week
Sunday:    Rest / content backlog production
```

## Measurement Framework

### Primary Metrics (per platform)
| Metric | Weight | Source |
|--------|--------|--------|
| View completion rate | 0.30 | Platform analytics |
| Engagement rate | 0.25 | (likes + comments + shares) / views |
| Share rate | 0.20 | shares / views |
| Follower conversion | 0.15 | new followers / views |
| Click-through rate | 0.10 | link clicks / views |

### Composite Score
```
score = (completion * 0.30) + (engagement * 0.25) + (share_rate * 0.20) + (follower_conv * 0.15) + (ctr * 0.10)
```

### Statistical Significance
- Minimum sample: 200 views per variant before analysis
- Confidence level: 95% (z = 1.96)
- Use two-proportion z-test for rate comparisons
- Report effect size (Cohen's h) alongside p-value

## Experiment Pydantic Model

Experiments are tracked using version-controlled Pydantic models (see `models/` directory):

```python
class Experiment:
    experiment_id: str          # UUID
    week_number: int            # ISO week
    hypothesis: str             # What we expect to learn
    variable: str               # What we're testing
    variant_a: VariantConfig    # Control
    variant_b: VariantConfig    # Treatment
    platforms: list[Platform]   # Where to deploy
    status: ExperimentStatus    # planned | running | completed | archived
    results: ExperimentResults  # Populated after analysis
```

## Reporting

### Weekly Report Template
```markdown
## Week {N} Experiment Report

### Hypothesis
{hypothesis}

### Variable Tested
{variable}: {variant_a.label} vs {variant_b.label}

### Results
| Platform | Variant A Score | Variant B Score | Winner | p-value | Effect Size |
|----------|----------------|----------------|--------|---------|-------------|

### Conclusion
{statistical interpretation}

### Action
{what changes to make based on results}

### Next Experiment
{what to test next week}
```

## Experiment Backlog
Maintain a prioritized backlog of experiments:
1. Hook type optimization (Week 1-2)
2. Optimal video duration (Week 3-4)
3. Posting time optimization (Week 5-6)
4. Visual style testing (Week 7-8)
5. CTA effectiveness (Week 9-10)
6. Platform-specific optimization (Week 11-12)
