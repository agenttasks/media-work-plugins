---
name: youtube-integration
description: |
  YouTube Data API v3 integration for uploading Shorts content.
  Handles OAuth, resumable uploads, metadata optimization, and analytics.
allowed-tools: Read, Write, Bash
---

# YouTube Integration

Upload and manage Shorts via YouTube Data API v3.

## API Reference

### Authentication
- Google OAuth 2.0
- Scopes: `youtube.upload`, `youtube.readonly`, `youtube.force-ssl`
- Refresh token for long-lived access
- Base URL: `https://www.googleapis.com/youtube/v3`

### Shorts Upload Flow (Resumable Upload)

#### Step 1: Initialize Upload
```
POST /upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,contentDetails
Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json
  X-Upload-Content-Length: <file-size-bytes>
  X-Upload-Content-Type: video/mp4
Body:
  {
    "snippet": {
      "title": "<title with #Shorts>",
      "description": "<description with keywords>",
      "tags": ["ClaudeCode", "AI", "Shorts"],
      "categoryId": "28",
      "defaultLanguage": "en"
    },
    "status": {
      "privacyStatus": "public",
      "selfDeclaredMadeForKids": false,
      "publishAt": "<ISO-8601>" (for scheduled)
    }
  }
Response Headers:
  Location: <resumable-upload-uri>
```

#### Step 2: Upload Video
```
PUT <resumable-upload-uri>
Headers:
  Content-Length: <chunk-size>
  Content-Range: bytes <start>-<end>/<total>
  Content-Type: video/mp4
Body: <binary video data>
```

#### Step 3: Verify Upload
```
GET /youtube/v3/videos?part=status&id=<video-id>
Response: { "items": [{ "status": { "uploadStatus": "processed" } }] }
```

### Shorts-Specific Requirements
- **Duration**: Up to 60 seconds
- **Aspect ratio**: 9:16 (vertical) - REQUIRED for Shorts classification
- **Title**: Include `#Shorts` in title or description for Shorts shelf placement
- **Resolution**: 1080x1920 recommended
- **Format**: MP4, MOV, AVI, WMV, FLV, 3GPP, MPEG4, WebM
- **File size**: Max 256GB (but keep under 100MB for Shorts)

### Quota System
- Daily quota: 10,000 units
- Video upload: 1,600 units per upload
- ~6 uploads per day with default quota
- List videos: 1 unit per call
- Update video: 50 units per call

### Analytics
```
GET /youtube/v3/videos?part=statistics&id=<video-id>
Response:
  statistics: {
    viewCount, likeCount, commentCount, favoriteCount
  }
```

For detailed analytics, use YouTube Analytics API:
```
GET /youtube/analytics/v2/reports
Dimensions: video
Metrics: views, estimatedMinutesWatched, averageViewDuration,
         averageViewPercentage, likes, shares, subscribersGained
```

## Upload Workflow

1. Validate video is vertical (9:16) and under 60 seconds
2. Prepare metadata with `#Shorts` tag
3. Initialize resumable upload
4. Upload video in chunks (5MB chunks recommended)
5. Poll processing status until complete
6. Record video_id for analytics
7. Update requirement status to completed

## SEO Optimization for Shorts
- Title: Keyword-rich, include `#Shorts`, under 100 characters
- Description: Include timestamps, links, and keywords
- Tags: Mix broad and specific (max 500 characters total)
- Thumbnail: Auto-generated from video (custom thumbnails for Shorts coming)
- Category: Science & Technology (ID: 28)

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `quotaExceeded` | Daily quota used | Queue for next day |
| `uploadLimitExceeded` | Too many uploads | Wait and retry |
| `forbidden` | Auth/permission issue | Refresh credentials |
| `videoRejected` | Policy violation | Review content, notify marketing |
| `processingFailure` | Server-side error | Retry upload |
