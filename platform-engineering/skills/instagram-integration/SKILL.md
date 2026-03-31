---
name: instagram-integration
description: |
  Instagram Graph API integration for publishing Reels via Meta Business Suite.
  Handles media upload, metadata, scheduling, and insights collection.
allowed-tools: Read, Write, Bash
---

# Instagram Integration

Upload and manage Reels content via Instagram Graph API (Meta Business Suite).

## API Reference

### Authentication
- Facebook/Meta OAuth 2.0
- Long-lived access token (60-day expiry, auto-refresh)
- Required permissions: `instagram_content_publish`, `instagram_basic`, `pages_read_engagement`
- Base URL: `https://graph.facebook.com/v19.0`

### Reels Publishing Flow

#### Step 1: Create Media Container
```
POST /{ig-user-id}/media
Parameters:
  media_type: REELS
  video_url: <publicly-accessible-url>
  caption: <text with hashtags and mentions>
  share_to_feed: true
  cover_url: <thumbnail-url> (optional)
  thumb_offset: <ms> (optional)
  location_id: <location-id> (optional)
  collaborators: [<username>] (optional)
  audio_name: <audio-track-name> (optional)
Response: { "id": "<creation-id>" }
```

#### Step 2: Check Container Status
```
GET /{creation-id}?fields=status_code
Response: { "status_code": "FINISHED" | "IN_PROGRESS" | "ERROR" }
```
Poll until FINISHED (typically 30-120 seconds).

#### Step 3: Publish
```
POST /{ig-user-id}/media_publish
Parameters:
  creation_id: <creation-id>
Response: { "id": "<media-id>" }
```

### Scheduled Publishing
```
POST /{ig-user-id}/media
Parameters:
  media_type: REELS
  video_url: <url>
  caption: <text>
  is_carousel_item: false
  published: false  # Creates draft
```
Note: Scheduling requires Meta Business Suite UI or separate scheduling service.

### Content Requirements
- **Format**: MP4, MOV
- **Codec**: H.264, H.265
- **Resolution**: 1080x1920 recommended (minimum 540x960)
- **Duration**: 3-90 seconds for Reels
- **File size**: Max 1GB
- **Frame rate**: 30fps recommended
- **Aspect ratio**: 9:16 (vertical), 1:1, 4:5 also supported

### Insights Collection
```
GET /{media-id}/insights
Metrics: impressions, reach, plays, likes, comments, shares, saved
Period: lifetime
```

### Rate Limits
- 25 content publishing API calls per 24-hour period
- 200 API calls per hour (general)
- Media container creation: 50/hour

## Upload Workflow

1. Validate video meets Instagram Reels specs
2. Host video at publicly accessible URL (or use presigned URL)
3. Create media container with caption and metadata
4. Poll container status until FINISHED
5. Publish the container
6. Record media_id for insights tracking
7. Update requirement status to completed

## Caption Best Practices
- Front-load the hook in first line (visible before "...more")
- Include 20-30 relevant hashtags (mix of sizes)
- Add CTA in caption body
- Tag relevant accounts (@anthropic, @claudeai)
- Include line breaks for readability

## Error Handling

| Error Code | Meaning | Action |
|-----------|---------|--------|
| `EXPIRED` | Container expired | Recreate container |
| `ERROR` | Processing failed | Check video specs, retry |
| `OAuthException` | Auth issue | Refresh token |
| `RATE_LIMIT` | Too many calls | Back off and retry |
