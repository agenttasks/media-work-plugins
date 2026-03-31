---
name: remote-control-ops
description: |
  Enables remote operation of content pipeline sessions from claude.ai/code
  or the Claude mobile app. Continue local work from any device while
  maintaining full access to MCP servers, files, and project configuration.
allowed-tools: Read Write Bash Grep Glob
metadata:
  trigger: remote-control
  platforms: web,mobile
---

# Remote Control Operations

Drive running content pipeline sessions from claude.ai/code or the Claude mobile app. Your full local environment — MCP servers, API keys, files — stays available.

## When to Use

- Monitor a long-running content generation pipeline from your phone
- Approve or reject content briefs from the web interface
- Adjust experiment parameters mid-run
- Check pipeline status and fix issues remotely

## Remote Control Workflow

### 1. Start Local Session
```bash
claude remote-control
```
This starts a session that can be controlled from claude.ai/code or the mobile app.

### 2. Connect Remotely
Navigate to claude.ai/code or open the Claude mobile app. The session syncs automatically across all connected devices.

### 3. Remote Operations

#### Pipeline Monitoring
```
Show me the current content pipeline status:
- Pending requirements count
- Active Higgsfield jobs
- Scheduled uploads for today
```

#### Content Approval
```
Review the latest content brief for Instagram.
Check the hook word count and hashtag format.
Approve if valid, flag issues if not.
```

#### Experiment Adjustment
```
The TikTok experiment has enough views.
Mark experiment EXP-2025-W10 as completed
and run the statistical analysis.
```

## Session Persistence

- Remote sessions automatically reconnect on network interruption
- All local MCP servers (Higgsfield) remain accessible
- File system operations work against the local project
- Git operations run on the local repository

## Access Control

- Remote control requires authenticated session pairing
- Operations are logged to telemetry for audit
- Destructive operations still require explicit confirmation
