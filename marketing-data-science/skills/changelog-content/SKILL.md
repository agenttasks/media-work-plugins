---
name: changelog-content
description: |
  Parses anthropics/claude-code CHANGELOG.md to extract daily updates and transforms them
  into social media content briefs for Instagram, TikTok, and YouTube Shorts.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# CHANGELOG Content Extraction

This skill reads the official `anthropics/claude-code` CHANGELOG.md and produces daily content briefs.

## Source

Fetch the latest CHANGELOG from:
!`curl -s https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | head -200`

## Extraction Process

1. **Parse CHANGELOG** - Extract entries by date, grouping by:
   - New features
   - Bug fixes
   - Breaking changes
   - Performance improvements

2. **Prioritize by Impact** - Rank entries by user impact:
   - HIGH: New capabilities, major UX changes
   - MEDIUM: Performance improvements, new integrations
   - LOW: Bug fixes, minor tweaks

3. **Generate Content Brief** per entry:

```yaml
changelog_date: "YYYY-MM-DD"
headline: "<attention-grabbing 1-liner>"
hook: "<first 3 seconds script for short-form video>"
key_points:
  - "<point 1>"
  - "<point 2>"
  - "<point 3>"
talking_points: "<30-second script>"
cta: "<call to action>"
hashtags:
  - "#ClaudeCode"
  - "#AI"
  - "#CodingWithAI"
platforms:
  instagram_reel: "<platform-specific adaptation>"
  tiktok: "<platform-specific adaptation>"
  youtube_short: "<platform-specific adaptation>"
```

## Content Calendar

- Generate a 7-day rolling content calendar from CHANGELOG entries
- Map entries to optimal posting times per platform
- Ensure no duplicate coverage across platforms on same day
- Stagger platform posts: TikTok (morning) -> Instagram (midday) -> YouTube (evening)

## Quality Gates

- Every brief must include a hook under 3 seconds read time
- Scripts must be under 60 seconds for Shorts/Reels/TikToks
- All technical claims must be traceable to a specific CHANGELOG entry
- Include source commit/PR reference for accuracy
