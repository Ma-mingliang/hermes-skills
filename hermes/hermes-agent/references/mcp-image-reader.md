# mcp-image-reader MCP Server

## 概述
将 mimo-v2.5 的图片理解能力封装为 Claude Code / Hermes 可调用的 MCP Tool。

## 安装信息
- 仓库：`D:\openclaw-hermes\mcp-image-reader`
- 来源：github.com/CYF1017/mcp-image-reader
- 技术栈：Python 3.9（零外部依赖）

## 配置
已添加到 `~/.hermes/config.yaml`：
```yaml
mcp_servers:
  image-reader:
    command: python
    args:
    - "D:\\openclaw-hermes\\mcp-image-reader\\server.py"
    env:
      MIMO_API_KEY: ${MIMO_API_KEY}
      MIMO_BASE_URL: https://token-plan-sgp.xiaomimimo.com/v1
```

## 使用方法
- "请读取 C:\path\to\image.png 的内容"
- "帮我看看这张截图"
- "描述一下桌面上的图片"

## 工具参数
| 参数 | 必填 | 说明 |
|------|------|------|
| image_path | 是 | 图片文件的绝对路径 |
| prompt | 否 | 自定义提示语，默认为"请详细描述这张图片的内容" |

## 注意事项
- mimo-v2.5-pro 不支持图片输入，需要用 mimo-v2.5（非 pro）
- 工作原理：读取本地图片 → base64 编码 → 调用 mimo-v2.5 API → 返回文字描述
- 如果遇到 "model not exist" 错误，检查是否在 mimo-v2.5-pro 下使用了图片
