---
name: generate-video
description: |
  Generate video content using Higgsfield AI from a requirement specification.
  Supports talking avatars, AI video generation, and UGC-style content.
allowed-tools: Read, Write, Bash
---

# Generate Video via Higgsfield

1. Read requirement from `requirements/accepted/` directory
2. Use the `higgsfield-mcp` skill to select appropriate generation mode
3. Call Higgsfield MCP server to generate video
4. Post-process (camera controls, upscale if needed)
5. Validate output against content spec requirements
6. Store generated video and update requirement status

Arguments:
- `$1`: Requirement ID or path to requirement YAML file
