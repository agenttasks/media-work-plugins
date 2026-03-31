---
name: integration-platform
description: |
  Core integration platform skill managing cross-service orchestration.
  Coordinates Higgsfield video generation with social media upload pipelines
  and measurement data collection.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Integration Platform

Orchestrates the end-to-end pipeline from video generation to content publishing.

## Pipeline Architecture

```
Requirement Received
    │
    ├─► Video Generation (Higgsfield MCP)
    │       │
    │       ├─► Generate video from script + style params
    │       ├─► Apply camera controls and effects
    │       ├─► Upscale if requested
    │       └─► Output: video file + metadata
    │
    ├─► Content Processing
    │       │
    │       ├─► Validate video specs (duration, resolution, codec)
    │       ├─► Generate platform-specific thumbnails
    │       ├─► Prepare metadata per platform
    │       └─► Output: platform-ready packages
    │
    ├─► Upload Pipeline
    │       │
    │       ├─► TikTok Content Posting API
    │       ├─► Instagram Graph API (Reels)
    │       └─► YouTube Data API v3 (Shorts)
    │
    └─► Measurement Setup
            │
            ├─► Configure analytics tracking
            ├─► Set up webhook listeners (if available)
            └─► Initialize experiment tracking params
```

## Service Health Checks

At session start, verify:
```bash
# Check Higgsfield MCP
# Check TikTok API credentials
# Check Instagram/Meta API credentials
# Check YouTube/Google API credentials
```

## Rate Limit Management

| Service | Rate Limit | Strategy |
|---------|-----------|----------|
| Higgsfield | Varies by plan | Queue with backoff |
| TikTok | 6 videos/day (unverified app) | Batch and schedule |
| Instagram | 25 API calls/day (publishing) | Priority queue |
| YouTube | 10,000 units/day | Cost-aware scheduling |

## Error Recovery

- Transient failures: Retry with exponential backoff (max 3 retries)
- Auth failures: Alert user, block requirement, log to telemetry
- Rate limits: Queue and schedule for next available window
- Content policy violations: Block requirement, notify marketing-data-science

## Configuration

Platform engineering reads its config from:
- `.mcp.json` for MCP server connections
- `.env.platform` for API credentials
- `config/rate-limits.yaml` for rate limit overrides
- `config/upload-defaults.yaml` for default upload parameters
