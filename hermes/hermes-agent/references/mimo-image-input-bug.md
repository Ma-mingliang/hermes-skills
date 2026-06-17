# mimo-v2.5-pro Image Input Bug (2026-06-02)

## Problem

`mimo-v2.5-pro` fails with: "There's an issue with the selected model (mimo-v2.5-pro). It may not exist or you may not have access to it."

## Root Cause

**OpenGateway middleware strips Authorization header** when request body contains image content (base64 images, screenshots).

- Auth PASSES when request body has NO message content
- Auth FAILS (401) when body contains actual messages with images
- Affects both `/v1/chat/completions` and `/v1/messages` routes

## Trigger Conditions

1. Using `mimo-v2.5` model and reading an image with Read tool
2. Using `mcp-chrome-tool` to capture screenshots
3. Any tool that injects image data into conversation history
4. Then switching to `mimo-v2.5-pro` — the image history persists

## Workarounds

| Approach | How |
|----------|-----|
| New conversation | Start fresh session without image history |
| Avoid images in mimo-v2.5 | Use other models for image tasks |
| Use mimo-v2.5 (non-pro) | It handles images correctly |
| Direct Xiaomi API | Bypass OpenGateway entirely |

## GitHub Issues

- Gitlawb/openclaude#1362 — Root cause: middleware strips auth header
- Gitlawb/openclaude#1343 — This specific error message
- Gitlawb/openclaude#1345 — OpenGateway revoked free mimo-v2.5
- anthropics/claude-code#62487 — Same bug in Claude Code

## Status

Open (as of 2026-06-02). Server-side fix needed in OpenGateway.
