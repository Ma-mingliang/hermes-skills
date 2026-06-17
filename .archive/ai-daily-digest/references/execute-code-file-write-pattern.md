# execute_code 文件写入模式

> 当 write_file 因 WSL 连接问题失败时的替代方案

## 问题

在 Windows 主机上，Hermes 的 `write_file` 工具走 WSL 路径。当 WSL 服务不可用时，所有文件操作都会失败：

```
wsl: 无法与 localhost 建立连接
execvpe(/bin/bash) failed: No such file or directory
```

## 解决方案

使用 `execute_code` + Python `open().write()` 直接写入，完全绕过 WSL：

```python
import os

# 确保目录存在
os.makedirs("D:/openclaw-hermes/data/daily/2026-05-31", exist_ok=True)

# 写入文件
content = "报告内容..."
with open("D:/openclaw-hermes/data/daily/2026-05-31/report.md", "w", encoding="utf-8") as f:
    f.write(content)

print(f"文件已保存，长度: {len(content)} 字符")
```

## 适用场景

- 保存日报报告到本地
- 写入大型文件（>10KB）
- 任何 write_file 失败的情况

## 注意事项

- 必须指定 `encoding="utf-8"` 处理中文
- 使用 `os.makedirs(..., exist_ok=True)` 确保目录存在
- 使用正斜杠路径 `D:/path/to/file` 或原始字符串 `r"D:\path\to\file"`

## 验证日期

2026-05-31：在 AI 日报任务中验证成功，成功写入 9978 字符的报告文件
