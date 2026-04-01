---
name: generate-content
description: |
  Generate social media content briefs from the latest Claude Code CHANGELOG updates.
  Produces platform-specific scripts for Instagram Reels, TikTok, and YouTube Shorts.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Generate Content from CHANGELOG

1. Use the `changelog-content` skill to fetch and parse the latest CHANGELOG.md
2. Use the `content-strategy` skill to create platform-specific adaptations
3. Validate all outputs against Pydantic ContentBrief model
4. Write content briefs to `output/briefs/`
5. If ready for production, use `requirements-handoff` to send to platform-engineering

Arguments:
- `$1`: Number of days to look back (default: 7)
- `$2`: Platform filter (default: all) - instagram, tiktok, youtube
