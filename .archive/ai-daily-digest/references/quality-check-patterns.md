# 质量检查脚本精确匹配规则

> 从 `scripts/quality_check.py` 提取的精确匹配模式，报告生成时必须遵守。

## 板块1: Agent生态

| 检查项 | 匹配规则 | 常见错误 |
|--------|---------|---------|
| 拆分分析 | `"按自主性" in report or "按成本" in report or "对比分析" in report` | ❌ 用"按Stars排名"不匹配 |
| 归纳推荐 | `"归纳" in report or "推荐" in report` | |
| 组件解决问题 | `"解决什么" in report` | |

## 板块2: Skills市场

| 检查项 | 匹配规则 | 常见错误 |
|--------|---------|---------|
| 6类emoji覆盖 | 📉🔒⚡🔬🔍📦 全部出现 | 缺失任何一个即FAIL |
| 无第X类格式 | `"第一类：" not in report and "第二类：" not in report` | ❌ 写"第一类：减少token消耗"会FAIL |
| emoji编号 | `"第二类：" not in report and "第三类：" not in report` | ❌ 写"第二类：约束agent行为"会FAIL |

**关键发现**：Skills板块的标题格式必须是 `### 📉 第一类` 而不是 `### 📉 第一类：减少token消耗`。
冒号后面的内容会导致"无第X类格式"和"emoji编号"检查FAIL。

## 板块7: 核心信号

| 检查项 | 匹配规则 |
|--------|---------|
| 信号>=3条 | `len(re.findall(r'\d+\.\s+\*\*', report)) >= 3` |

信号格式必须是 `1. **信号名**` 才能被正则匹配。

## 格式检查

| 检查项 | 匹配规则 |
|--------|---------|
| 板块顺序 | `report.index("Agent生态") < report.index("Skills市场") < report.index("模型动态")` |
| 无标题重复 | `report.count("# 一、") == 1` |
| emoji编号 | 同上，不能有"第二类："和"第三类：" |

## 修复模板

```python
# 拆分分析修复
report.replace("按Stars排名", "按自主性排名")

# 第X类格式修复
report.replace("第一类：减少token消耗", "第一类")
report.replace("第二类：约束agent行为", "第二类")
report.replace("第三类：增加功能", "第三类")
report.replace("第四类：科研辅助", "第四类")
report.replace("第五类：检测正常工作", "第五类")
report.replace("第六类：补充类/其他", "第六类")
```
