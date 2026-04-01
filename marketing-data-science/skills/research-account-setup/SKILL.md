---
name: research-account-setup
description: |
  Research and account setup skill for social media platforms. Guides through
  API registration, developer account creation, and initial configuration for
  TikTok, Instagram, and YouTube content publishing.
allowed-tools: Read, Write, Bash
---

# Research & Account Setup

## Platform Account Requirements

### TikTok
1. **Creator Account**: Upgrade to TikTok Creator or Business account
2. **Developer Portal**: Register at developers.tiktok.com
3. **App Registration**: Create app for Content Posting API
   - Scopes: `video.publish`, `video.upload`
   - Requires app review and approval (5-10 business days)
4. **Environment Variables**:
   ```
   TIKTOK_CLIENT_KEY=<app-key>
   TIKTOK_CLIENT_SECRET=<app-secret>
   TIKTOK_ACCESS_TOKEN=<oauth-token>
   ```

### Instagram (via Meta Business Suite)
1. **Business Account**: Convert to Instagram Business or Creator account
2. **Facebook Page**: Link Instagram to a Facebook Page
3. **Meta Developer Portal**: Register at developers.facebook.com
4. **App Registration**: Create app with Instagram Graph API
   - Permissions: `instagram_content_publish`, `pages_read_engagement`
   - Requires app review for publishing permissions
5. **Environment Variables**:
   ```
   META_APP_ID=<app-id>
   META_APP_SECRET=<app-secret>
   INSTAGRAM_ACCESS_TOKEN=<long-lived-token>
   INSTAGRAM_BUSINESS_ACCOUNT_ID=<account-id>
   ```

### YouTube (via Google Cloud)
1. **YouTube Channel**: Create or use existing channel
2. **Google Cloud Console**: Create project at console.cloud.google.com
3. **Enable YouTube Data API v3**
4. **OAuth 2.0 Credentials**: Create OAuth client for desktop app
   - Scopes: `youtube.upload`, `youtube.readonly`
5. **Environment Variables**:
   ```
   GOOGLE_CLIENT_ID=<client-id>
   GOOGLE_CLIENT_SECRET=<client-secret>
   YOUTUBE_REFRESH_TOKEN=<refresh-token>
   YOUTUBE_CHANNEL_ID=<channel-id>
   ```

### Higgsfield AI
1. **Account**: Sign up at higgsfield.ai
2. **API Access**: Request API key from settings or contact page
3. **Plan**: Verify sufficient credits for video generation
4. **Environment Variables**:
   ```
   HIGGSFIELD_API_KEY=<api-key>
   ```

## Setup Verification Checklist

Run this verification at session start:
```bash
# Check all required environment variables
for var in TIKTOK_CLIENT_KEY META_APP_ID GOOGLE_CLIENT_ID HIGGSFIELD_API_KEY; do
  if [ -z "${!var}" ]; then
    echo "MISSING: $var"
  else
    echo "OK: $var"
  fi
done
```

## Research Tasks

When setting up a new platform, research:
1. Current API rate limits and quotas
2. Content policy and community guidelines
3. Optimal content specifications (resolution, codec, bitrate)
4. Analytics API availability for measurement
5. Webhook availability for real-time notifications

## Handoff

After account setup is complete, generate a requirements document for platform-engineering:
- Confirmed API access per platform
- Rate limits and quotas discovered
- Content specifications validated
- Credentials stored securely (never in version control)
