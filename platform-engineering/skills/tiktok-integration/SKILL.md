---
name: tiktok-integration
description: |
  TikTok Content Posting API integration for uploading short-form video content.
  Handles OAuth, video upload, metadata, and scheduling via TikTok Developer API.
allowed-tools: Read, Write, Bash
---

# TikTok Integration

Upload and manage content via TikTok's Content Posting API.

## API Reference

### Authentication
- OAuth 2.0 flow with PKCE
- Scopes: `video.publish`, `video.upload`, `video.list`
- Token refresh: Automatic before expiry
- Base URL: `https://open.tiktokapis.com/v2`

### Video Upload Flow

#### Step 1: Initialize Upload
```
POST /post/publish/inbox/video/init/
Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json
Body:
  {
    "source_info": {
      "source": "FILE_UPLOAD",
      "video_size": <bytes>,
      "chunk_size": <bytes>,
      "total_chunk_count": <int>
    }
  }
Response: { "publish_id": "...", "upload_url": "..." }
```

#### Step 2: Upload Video Chunks
```
PUT {upload_url}
Headers:
  Content-Range: bytes {start}-{end}/{total}
  Content-Type: video/mp4
Body: <binary video data>
```

#### Step 3: Publish
```
POST /post/publish/video/init/
Body:
  {
    "post_info": {
      "title": "<caption with hashtags>",
      "privacy_level": "PUBLIC_TO_EVERYONE",
      "disable_duet": false,
      "disable_comment": false,
      "disable_stitch": false,
      "video_cover_timestamp_ms": 1000
    },
    "source_info": {
      "source": "PULL_FROM_URL",
      "video_url": "<hosted-video-url>"
    }
  }
```

### Content Requirements
- **Format**: MP4, WebM
- **Codec**: H.264
- **Resolution**: 720x1280 minimum, 1080x1920 recommended
- **Duration**: 3-600 seconds (Shorts: 15-60s)
- **File size**: Max 4GB
- **Aspect ratio**: 9:16 for vertical

### Rate Limits
- Unverified apps: 6 videos/day
- Verified apps: Higher limits (varies)
- API calls: 100 requests/minute

## Upload Workflow

1. Validate video meets TikTok specs
2. Generate caption from ContentBrief (include hashtags)
3. Initialize upload session
4. Upload video (chunked for large files)
5. Set metadata and privacy
6. Publish or schedule
7. Record publish_id for analytics tracking
8. Update requirement status to completed

## Error Handling

| Error Code | Meaning | Action |
|-----------|---------|--------|
| `spam_risk_too_many_posts` | Rate limited | Queue for next day |
| `video_file_wrong_format` | Invalid format | Re-encode with ffmpeg |
| `access_token_invalid` | Auth expired | Refresh token and retry |
| `scope_not_authorized` | Missing permissions | Alert user to reauthorize |
