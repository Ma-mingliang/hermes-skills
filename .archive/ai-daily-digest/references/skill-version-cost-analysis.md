# SKILL版本成本分析（2026-05-30）

## 定价
- 输入命中缓存：0.025元/1M tokens
- 输入未命中：3元/1M tokens
- 输出：6元/1M tokens
- 缓存命中率：97%

## SKILL文件大小

| 版本 | 文件大小 | 预估Token |
|------|----------|-----------|
| SKILL-core.md | 1,952字符 | ~1,366 tokens |
| SKILL-balanced.md | 9,443字符 | ~6,610 tokens |
| SKILL-full.md | 40,984字符 | ~28,688 tokens |

## 运行成本（含系统提示+用户提示+Agent推理+输出）

| 版本 | 每次成本 | 每日成本 | 每月成本 |
|------|----------|----------|----------|
| Core | ~0.059元 | ~0.059元/天 | ~1.77元/月 |
| Balanced | ~0.123元 | ~0.123元/天 | ~3.67元/月 |
| Full | ~0.390元 | ~0.390元/天 | ~11.70元/月 |

## 联网操作不消耗Token

以下操作直接HTTP请求或本地计算，不经过LLM：
- 联网搜索（HN Algolia API、GitHub API）
- 网页抓取（web_fetch、browser）
- RSS解析（urllib获取XML）
- 数据处理（Python代码）
- 文件读写（read_file、write_file）

## 推荐

- 日常使用：Balanced版本（3.67元/月）
- 快速测试：Core版本（1.77元/月）
- 详细参考：Full版本（11.70元/月）
