# Skill Backup Before Refactoring

When user says "备份" + skill name + "重构"/"refactor":

## Steps

1. **统计源目录**
   ```python
   # 列出目录结构 + 文件数 + 总大小
   for root, dirs, files in os.walk(skill_dir):
       ...
   ```

2. **创建带时间戳的备份目录**
   ```python
   backup_dir = f"D:/openclaw-hermes/backups/{skill_name}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
   shutil.copytree(skill_dir, backup_dir, dirs_exist_ok=True)
   ```

3. **创建 BACKUP_README.md**
   - 备份时间
   - 源目录
   - 文件数/总大小
   - 目录结构说明
   - 恢复方法

4. **创建 REFACTORING_PLAN.md**（如用户要求）
   - 当前版本优缺点
   - 重构方向
   - 分阶段计划
   - 预期效果
   - 风险与应对

5. **更新备份清单**
   ```python
   manifest_path = f"D:/openclaw-hermes/backups/backup_manifest.json"
   # 记录所有备份
   ```

6. **更新 memory**（如空间允许）
   - 记录备份位置和文件数

## Backup Location Convention

```
D:/openclaw-hermes/backups/{skill-name}-{YYYYMMDD_HHMMSS}/
├── SKILL.md
├── scripts/
├── references/
├── checklists/
├── BACKUP_README.md
├── REFACTORING_PLAN.md  (optional)
└── ...
```

## Pitfalls

- memory 可能已满，无法添加新条目 → replace 现有条目添加备份信息
- 备份目录不要用中文冒号等特殊字符
- 恢复时注意覆盖问题
