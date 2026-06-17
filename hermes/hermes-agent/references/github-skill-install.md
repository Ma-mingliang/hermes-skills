# 从 GitHub 安装第三方 Skill

## 方法

```python
import subprocess, os, shutil

# 1. 克隆仓库
repo_url = "https://github.com/<owner>/<repo>.git"
target = os.path.expanduser(r"~\temp\<repo-name>")
subprocess.run(["git", "clone", repo_url, target], capture_output=True, text=True, timeout=120)

# 2. 找到 skill 目录（通常在 skills/<name>/ 下）
skill_source = os.path.join(target, "skills", "<name>")
skill_dest = os.path.expanduser(r"~\.hermes\skills\<name>")

# 3. 复制到 Hermes skills 目录
if os.path.exists(skill_dest):
    shutil.rmtree(skill_dest)
shutil.copytree(skill_source, skill_dest)

# 4. 清理临时目录（可选）
# shutil.rmtree(target)
```

## Pitfalls

- **WSL relay 问题**：Windows 上 `terminal` 工具的 bash 可能因 WSL NAT 错误失败。使用 Python `subprocess.run()` + `capture_output=True` 替代。
- **skill 目录结构**：标准结构是 `skills/<name>/SKILL.md`，但有些仓库是扁平的 `<name>/SKILL.md`。先用 `os.walk()` 探索目录结构。
- **依赖检查**：安装后检查 skill 的 `metadata.requires.bins` 中列出的命令是否可用（如 `python3`、`node`）。
- **验证安装**：用 `skill_view(name='<name>')` 确认加载成功。
- **Python3 命令**：Windows 上通常是 `python` 而非 `python3`，某些 skill 的脚本可能硬编码了 `python3`。

## 示例（last30days-skill，2026-06-11）

```python
# 已验证：Python 3.12.3 + Node v24.16.0
# 克隆到 C:\Users\lenovo_mml\last30days-skill
# 安装到 C:\Users\lenovo_mml\.hermes\skills\last30days
# skill_view 加载成功
```
