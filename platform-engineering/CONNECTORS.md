# Connectors - Platform Engineering

## MCP Servers

| Server | Type | Purpose |
|--------|------|---------|
| Higgsfield | HTTP MCP | AI video and image generation |

## API Integrations

| Platform | API | Auth | Purpose |
|----------|-----|------|---------|
| TikTok | Content Posting API v2 | OAuth 2.0 + PKCE | Video upload and publishing |
| Instagram | Graph API v19.0 | Meta OAuth 2.0 | Reels publishing |
| YouTube | Data API v3 | Google OAuth 2.0 | Shorts upload |
| Higgsfield | MCP Server | API Key | Video/image generation |

## Environment Variables Required

```
# Higgsfield
HIGGSFIELD_API_KEY=

# TikTok
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=

# Instagram / Meta
META_APP_ID=
META_APP_SECRET=
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=

# YouTube / Google
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
YOUTUBE_CHANNEL_ID=
```

## Cross-Plugin Communication

| Direction | Channel | Format |
|-----------|---------|--------|
| marketing-data-science → platform-engineering | `requirements/pending/` | YAML (Requirement model) |
| platform-engineering → marketing-data-science | `requirements/completed/` | YAML (status update) |
