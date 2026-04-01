---
name: upload-content
description: |
  Upload generated video content to social media platforms (TikTok, Instagram, YouTube).
  Handles platform-specific upload flows, metadata, and scheduling.
allowed-tools: Read, Write, Bash
---

# Upload Content to Social Platforms

1. Read requirement from `requirements/accepted/` with upload_spec
2. Validate video meets platform-specific requirements
3. Route to appropriate integration skill:
   - TikTok: `tiktok-integration`
   - Instagram: `instagram-integration`
   - YouTube: `youtube-integration`
4. Execute platform upload flow
5. Record publish IDs for analytics tracking
6. Update requirement status to completed

Arguments:
- `$1`: Requirement ID or path to requirement YAML file
- `$2`: Platform override (optional) - tiktok, instagram, youtube
