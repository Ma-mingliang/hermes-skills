# MiMo v2.5 Pro Image Handling Bug

## Issue

MiMo v2.5-pro fails when processing images (screenshots, Read tool on images). Error:
```
There's an issue with the selected model (mimo-v2.5-pro). It may not exist or you may not have access to it.
```

## Root Cause

OpenGateway middleware strips Authorization header when requests contain image content. This is a server-side bug, not a model limitation.

## Affected Scenarios
- Attaching images as context
- Using mcp-chrome-tool for screenshots
- Reading image files with Read tool
- Any multimodal input

## Workarounds

1. **Use mimo-v2.5 (non-pro)** for image tasks - supports images without the bug
2. **Use mcp-image-reader** MCP server - routes image requests through mimo-v2.5
3. **New conversation** - start fresh without image history
4. **Avoid images in mimo-v2.5-pro sessions**

## GitHub Issues
- Gitlawb/openclaude#1343 - Original report
- Gitlawb/openclaude#1362 - Root cause (OpenGateway middleware)
- anthropics/claude-code#62487 - Claude Code specific

## Status
- OpenGateway bug: OPEN (server-side fix needed)
- Workaround: Use mimo-v2.5 for images or mcp-image-reader

## Related
- mcp-image-reader installed at `D:\openclaw-hermes\mcp-image-reader\`
- Configured in `~/.hermes/config.yaml` under `mcp_servers.image-reader`
