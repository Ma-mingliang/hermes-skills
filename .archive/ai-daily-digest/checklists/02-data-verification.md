# 数据验证执行清单

## 📋 执行前确认
- [ ] 数据收集已完成
- [ ] 已获取collection_log.json

## 🔍 数据验证清单

### 1. 时间戳验证（必须）
**目标**：验证所有数据是否是今日的

**GitHub项目验证**：
```python
# 检查每个项目的created_at
for project in github_projects:
    created_at = project["created_at"]  # 格式：2026-05-30T10:00:00Z
    if created_at < "2026-05-29":
        print(f"⚠️ 项目 {project['name']} 不是今日新增：{created_at}")
```

**验证清单**：
- [ ] GitHub项目：created_at是否是近7天
- [ ] HN帖子：created_at_i是否是今天（时间戳）
- [ ] 36氪新闻：发布时间是否是今天
- [ ] 模型官网：最后更新时间是否是近期

**输出**：
```
时间戳验证结果：
- GitHub：X个今日新增，Y个非今日（已过滤）
- HN：X个今日新增，Y个非今日（已过滤）
- 36氪：X个今日新增，Y个非今日（已过滤）
```

### 2. URL可访问性验证（必须）
**目标**：验证所有URL是否可访问

**验证方法**：
```python
import urllib.request

def verify_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except:
        return False
```

**验证清单**：
- [ ] GitHub项目URL：是否可访问（非404）
- [ ] HN帖子URL：是否可访问
- [ ] 36氪新闻URL：是否可访问
- [ ] 模型官网URL：是否可访问

**输出**：
```
URL验证结果：
- GitHub：X个可访问，Y个404（已过滤）
- HN：X个可访问，Y个不可访问（已过滤）
- 36氪：X个可访问，Y个不可访问（已过滤）
- 模型官网：X个可访问，Y个不可访问（已标记）
```

### 3. 数据真实性验证（必须）
**目标**：验证数据是否真实（非编造）

**GitHub项目验证**：
```python
# 对比GitHub API返回的stars和页面显示的stars
for project in github_projects:
    api_stars = project["stargazers_count"]
    # 访问GitHub页面获取真实stars
    page_stars = get_page_stars(project["html_url"])
    if abs(api_stars - page_stars) > 10:
        print(f"⚠️ 项目 {project['name']} stars数不一致：API={api_stars}, 页面={page_stars}")
```

**验证清单**：
- [ ] GitHub项目：stars数是否与页面一致
- [ ] HN帖子：热度（points）是否真实
- [ ] 模型版本：是否与官网一致
- [ ] 模型排名：是否与排行榜一致

**输出**：
```
数据真实性验证结果：
- GitHub：X个stars一致，Y个不一致（已标记）
- HN：X个热度真实，Y个存疑（已标记）
- 模型：X个版本一致，Y个不一致（已标记）
```

### 4. 分类验证（必须）
**目标**：验证分类是否准确

**验证方法**：
```python
# 检查同一个项目在不同搜索结果中的分类是否一致
for project in all_projects:
    classifications = get_classifications(project["name"])
    if len(set(classifications)) > 1:
        print(f"⚠️ 项目 {project['name']} 分类不一致：{classifications}")
```

**验证清单**：
- [ ] 同一项目：在不同搜索结果中的分类是否一致
- [ ] 描述关键词：是否与分类匹配
- [ ] 文件结构：是否与分类匹配（.md=Skills, .py=Agent）

**输出**：
```
分类验证结果：
- 一致：X个项目
- 不一致：Y个项目（已标记，需要重新分类）
```

## ✅ 执行确认

**数据验证完成后，必须输出以下确认信息**：
```
📊 数据验证完成确认
====================
1. 时间戳验证：X个今日数据，Y个非今日（已过滤）
2. URL验证：X个可访问，Y个不可访问（已过滤）
3. 真实性验证：X个真实，Y个存疑（已标记）
4. 分类验证：X个一致，Y个不一致（已重新分类）

总计：验证X个数据点，通过Y个，过滤Z个，标记W个
```

## ⚠️ 异常处理

**如果数据不是今日的**：
1. 过滤掉非今日数据
2. 记录过滤原因
3. 重新收集今日数据

**如果URL不可访问**：
1. 标记为"不可访问"
2. 尝试备用URL
3. 如果无备用URL，跳过该数据

**如果数据不真实**：
1. 标记为"存疑"
2. 使用备用数据源验证
3. 如果无法验证，不使用该数据

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/verification_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "timestamp_verification": {"today": 50, "not_today": 10, "filtered": 10},
  "url_verification": {"accessible": 45, "not_accessible": 5, "filtered": 5},
  "authenticity_verification": {"real": 40, "questionable": 5, "marked": 5},
  "classification_verification": {"consistent": 35, "inconsistent": 5, "reclassified": 5}
}
```
