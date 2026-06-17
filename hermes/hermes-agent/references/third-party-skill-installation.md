# 安装第三方Skill集合到Hermes

> 操作模式：clone → copy → verify → cleanup

## 标准流程

```python
import os, shutil, subprocess

hermes_dir = r"C:\Users\lenovo_mml\.hermes"
skills_dir = os.path.join(hermes_dir, "skills")

# 1. Clone到临时目录
temp_dir = os.path.join(hermes_dir, "temp_<name>")
subprocess.run(["git", "clone", "--depth", "1", "<repo_url>", temp_dir], timeout=120)

# 2. 定位skills源目录（不同仓库结构不同）
skills_source = os.path.join(temp_dir, "skills")  # ARIS结构
# 或 skills_source = temp_dir  # 直接就是skills目录

# 3. 复制到目标
target_dir = os.path.join(skills_dir, "<name>")
os.makedirs(target_dir, exist_ok=True)
for skill in os.listdir(skills_source):
    src = os.path.join(skills_source, skill)
    dst = os.path.join(target_dir, skill)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

# 4. 验证：检查SKILL.md存在
valid = sum(1 for s in os.listdir(target_dir) 
            if os.path.isfile(os.path.join(target_dir, s, "SKILL.md")))

# 5. 清理（Windows下.git可能锁定，用terminal rm -rf）
```

## 注意事项

- Windows下`shutil.rmtree`删除.git目录可能报PermissionError，用`terminal`的`rm -rf`替代
- 某些skills可能缺少SKILL.md（如shared-references目录、元数据目录），属于正常
- 安装后需更新memory中的skills计数
- 大批量安装影响prompt cache prefix，建议一次性完成

## 已安装的第三方集合

| 集合 | 数量 | 位置 | 来源 |
|------|------|------|------|
| ECC | 25 | ~/.hermes/skills/ecc/ | affaan-m/ECC |
| ARIS | 77 | ~/.hermes/skills/aris/ | wanshuiyin/Auto-claude-code-research-in-sleep |
| Cache优化 | 17 | ~/.hermes/skills/ | 各prompt-cache-* skills |

## 潜在候选（2026-05-29分析）

| 集合 | Stars | 技术路线 | 特点 |
|------|-------|---------|------|
| Orchestra Research AI-Research-SKILLs | 9,054 | 知识库 | 98个AI研究技能，23类别，工程导向 |
| Master-cai Research-Paper-Writing-Skills | 3,044 | 写作方法论 | 基于彭思达教授笔记，审稿人视角 |
| ClaudePrism | 1,515 | 本地优先桌面应用 | Tauri 2+Rust，离线LaTeX+Python |
| zLanqing codex-claude-academic-skills | 199 | 中文优先 | 三技能协作（写作+Office+计算）|

**选择建议**: 端到端ML研究用ARIS，AI工程用Orchestra，论文写作用Master-cai，中文用zLanqing

## 安装后验证

```python
# 统计有效skills（有SKILL.md的）
valid = sum(1 for s in os.listdir(target_dir) 
            if os.path.isfile(os.path.join(target_dir, s, "SKILL.md")))
total = sum(1 for s in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, s)))
print(f"有效: {valid}/{total}")
```

常见缺失SKILL.md的目录：shared-references（共享参考文档）、skills-codex*（元数据目录）
