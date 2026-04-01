# Platform Engineering Plugin

Platform integration plugin for AI video generation via Higgsfield and social media
content upload pipelines (TikTok, Instagram, YouTube).

## Skills

| Skill | Description |
|-------|-------------|
| `requirements-receiver` | Receives and triages requirements from marketing-data-science |
| `integration-platform` | Core orchestration for video generation → upload pipeline |
| `higgsfield-mcp` | Higgsfield AI MCP integration for video/image generation |
| `tiktok-integration` | TikTok Content Posting API for video upload |
| `instagram-integration` | Instagram Graph API for Reels publishing |
| `youtube-integration` | YouTube Data API v3 for Shorts upload |

## Commands

| Command | Description |
|---------|-------------|
| `/platform-engineering:generate-video` | Generate video via Higgsfield from requirement |
| `/platform-engineering:upload-content` | Upload video to social media platforms |

## MCP Servers

| Server | Purpose |
|--------|---------|
| Higgsfield | AI video generation, lip-sync avatars, camera controls, upscaling |

## Pipeline

```
Requirement → Higgsfield Video Generation → Platform Upload → Analytics Tracking
                                                 ↓
                                    TikTok / Instagram / YouTube
```

## Installation

```bash
claude plugin marketplace add agenttasks/media-work-plugins
claude plugin install platform-engineering@media-work-plugins
```

## Required Setup

See [CONNECTORS.md](./CONNECTORS.md) for required API credentials and environment variables.
