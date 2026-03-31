---
name: content-strategy
description: |
  Multi-platform content strategy for daily shorts on Instagram Reels, TikTok, and YouTube Shorts.
  Focuses on Claude Code CHANGELOG updates with platform-specific optimization and audience targeting.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Content Strategy for Social Media Shorts

## Platform Specifications

### Instagram Reels
- **Duration**: 15-90 seconds (optimal: 30-45s)
- **Aspect ratio**: 9:16 (1080x1920)
- **Style**: Polished, branded, educational
- **Audience**: Professional developers, tech leads
- **Tone**: Authoritative yet accessible
- **Best posting**: Tue-Thu, 11am-1pm EST
- **Hashtag strategy**: Mix of broad (#AI, #coding) and niche (#ClaudeCode, #AIAssistant)

### TikTok
- **Duration**: 15-60 seconds (optimal: 21-34s)
- **Aspect ratio**: 9:16 (1080x1920)
- **Style**: Raw, fast-paced, trend-aware
- **Audience**: Junior developers, CS students, tech enthusiasts
- **Tone**: Casual, excited, "did you know" energy
- **Best posting**: Mon-Fri, 7am-9am EST
- **Hook requirement**: Must grab attention in first 1.5 seconds

### YouTube Shorts
- **Duration**: Up to 60 seconds (optimal: 30-45s)
- **Aspect ratio**: 9:16 (1080x1920)
- **Style**: Tutorial-like, demo-focused
- **Audience**: Mid-senior developers, content creators
- **Tone**: Informative, show-don't-tell
- **Best posting**: Wed-Fri, 2pm-4pm EST
- **SEO**: Title and description optimization for YouTube search

## Content Pillars

1. **Feature Drops** - New Claude Code capabilities (40% of content)
2. **Tips & Tricks** - Power user workflows (25% of content)
3. **Before/After** - Productivity comparisons (20% of content)
4. **Community Wins** - User stories and use cases (15% of content)

## Script Framework

```
HOOK (0-3s): Question or surprising statement from CHANGELOG
CONTEXT (3-10s): What changed and why it matters
DEMO (10-35s): Show the feature in action (screen recording or avatar)
CTA (35-45s): Try it yourself + follow for more
```

## Cross-Platform Adaptation Rules

- Same core message, different delivery per platform
- TikTok: More informal, use trending sounds
- Instagram: Add text overlays, use branded templates
- YouTube: Include chapter markers in description, keyword-rich title

## Handoff to Platform Engineering

When content strategy is finalized, create a structured requirement for platform-engineering:
- Video generation specs (Higgsfield parameters)
- Upload metadata per platform
- Scheduling requirements
- A/B variant specifications if applicable
