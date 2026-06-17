# WeChat Image Receiving Capability

## Overview

Hermes Agent can receive images sent via WeChat (微信). This capability enables workflows like automated image processing, analysis, and optimization.

## Technical Details

### Image Storage Location

When a user sends an image via WeChat, Hermes automatically:
1. Receives the image from WeChat's messaging API
2. Saves it to the local image cache directory
3. Provides the file path to the agent

**Storage path**: `~/.hermes/image_cache/`

**Filename format**: `img_{hash}.jpg`
- `{hash}` is a unique identifier (e.g., `2a45bda8a382`)
- Images are saved in JPEG format regardless of original format

### Example Path
```
C:\Users\<username>\.hermes\image_cache\img_2a45bda8a382.jpg
```

### Verification (2026-06-08)
- Tested with actual WeChat image send
- Image successfully received and saved
- File accessible via standard file operations

## Workflow Pattern: Auto Image Processing

### Architecture
```
User sends image via WeChat
    ↓
Hermes receives and saves to ~/.hermes/image_cache/
    ↓
Agent processes image (analyze, optimize, transform)
    ↓
Agent sends result back via MEDIA: protocol
```

### Integration with apikey-image-gen

The received image can be passed to `apikey-image-gen` skill for processing:

```json
{
  "mode": "image",
  "prompt": "优化这张图片...",
  "image_path": "~/.hermes/image_cache/img_{hash}.jpg",
  "output_path": "~/.hermes/image_cache/optimized_{hash}.jpg"
}
```

### Sending Results Back

Use the `MEDIA:` protocol to send processed images back to user:
```
MEDIA:/path/to/processed/image.jpg
```

## Known Issues

### vision_analyze API Key Error
- Error: `Invalid API Key` (401)
- May occur when using vision_analyze with local file paths
- Does not affect image receiving capability
- Workaround: Use mcp-image-reader or process image directly

## Use Cases

1. **Automated P图**: User sends image → Agent optimizes → Returns result
2. **Image Analysis**: User sends image → Agent describes content
3. **Batch Processing**: User sends multiple images → Agent processes all
4. **Format Conversion**: User sends image → Agent converts format

## Related Skills

- `apikey-image-gen`: Image generation and editing via API
- `mcp-image-reader`: Image reading via mimo-v2.5
- `vision_analyze`: Image analysis tool

## Future Enhancements

- [ ] Write auto-image-processing skill
- [ ] Support batch image processing
- [ ] Add image quality presets
- [ ] Support custom processing prompts
