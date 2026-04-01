---
name: higgsfield-mcp
description: |
  Manages read and write operations with Higgsfield AI MCP server for video and image generation.
  Supports talking avatars, lip-sync, camera controls, upscaling, and short ad creation.
allowed-tools: Read, Write, Bash
---

# Higgsfield MCP Integration

Manages all interactions with the Higgsfield AI platform for content generation.

## Capabilities

### Video Generation
- **AI Video Generation**: Create videos from text prompts
  - Endpoint: `https://higgsfield.ai/create/video`
  - Supports style transfer, scene composition, motion control
- **Talking Avatar with Lip-Sync**: Generate avatar videos synced to script audio
  - Endpoint: `https://higgsfield.ai/lipsync-studio`
  - Parameters: avatar_id, script, voice, motion_style
- **Draw-to-Video**: Convert sketches/storyboards to video
  - Endpoint: `https://higgsfield.ai/create/video?video-inpaint=true`
- **UGC Video**: User-generated content style with avatars
  - Endpoint: `https://higgsfield.ai/lipsync-studio?ugc-studio=true`

### Image Generation
- **AI Image Generation**: Create images from prompts
  - Endpoint: `https://higgsfield.ai/image/nano_banana_2`
- **Character Creation**: Design unique characters for consistent branding
  - Endpoint: `https://higgsfield.ai/character`
- **Inpainting**: Edit existing images seamlessly
  - Endpoint: `https://higgsfield.ai/edit?model=soul-canvas`

### Post-Processing
- **Upscale**: Enhance video/image quality
  - Endpoint: `https://higgsfield.ai/upscale`
- **Camera Controls**: Apply cinematic camera movements
  - Supported: zoom_in, zoom_out, pan_left, pan_right, orbit, dolly

### Short Ads
- **Product Placement Ads**: Create short ad formats
  - Endpoint: `https://higgsfield.ai/ads`
  - Uses predefined presets for quick generation

## MCP Server Configuration

The Higgsfield MCP server is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "higgsfield": {
      "type": "http",
      "url": "https://mcp.higgsfield.ai/v1"
    }
  }
}
```

## Content Generation Workflow

1. **Receive requirement** with content_spec and video_generation params
2. **Select generation mode** based on visual_style:
   - `talking_avatar` → Lip-Sync Studio
   - `screen_recording` → Not Higgsfield (local capture)
   - `text_overlay` → AI Video Generation + text overlay
   - `ugc_style` → UGC Video Studio
   - `short_ad` → Short Ads preset
3. **Generate content** via MCP tool call
4. **Post-process**: Apply camera controls, upscale if requested
5. **Validate output**: Check duration, resolution, file size
6. **Return** video file path and metadata

## Branding Consistency

- Create a persistent character/avatar for the brand using Character Creation
- Use consistent style parameters across all generations
- Store avatar_id and style presets in `config/brand.yaml`:

```yaml
brand:
  avatar_id: "<persistent-avatar-id>"
  default_style: "professional_tech"
  color_palette: ["#7C3AED", "#2563EB", "#10B981"]
  voice: "professional_male_1"
  motion_style: "natural"
```

## Cost Awareness

Track Higgsfield credit usage per generation:
- Standard video: ~2-5 credits
- Lip-sync avatar: ~5-10 credits
- Upscale: ~1-2 credits
- Log all costs to session telemetry
