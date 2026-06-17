# Crawlee SPA抓取方案（2026-05-31验证）

## 安装步骤

### 1. 安装Python包
```bash
pip install crawlee playwright browserforge
```

### 2. 安装浏览器
```bash
python -m playwright install
```

这会安装以下浏览器：
- Chrome for Testing 148.0.7778.96 (playwright chromium v1223)
- Chrome Headless Shell 148.0.7778.96
- Firefox 150.0.2 (playwright firefox v1522)
- WebKit 26.4 (playwright webkit v2287)
- FFmpeg (playwright ffmpeg v1011)
- Winldd (playwright winldd v1007)

### 3. 验证安装
```python
import crawlee
print(f"crawlee版本: {crawlee.__version__}")

from crawlee.crawlers import PlaywrightCrawler
print("PlaywrightCrawler导入成功")
```

## 使用示例

### 基本用法
```python
import asyncio
from crawlee.crawlers import PlaywrightCrawler

async def main():
    crawler = PlaywrightCrawler(headless=True, browser_type='chromium')
    
    @crawler.router.default_handler
    async def request_handler(context):
        await context.page.wait_for_load_state('networkidle')
        title = await context.page.title()
        content = await context.page.content()
        print(f"页面标题: {title}")
        print(f"页面内容长度: {len(content)} 字符")
    
    await crawler.run(['https://github.com/trending'])

asyncio.run(main())
```

### 提取表格数据
```python
import asyncio
from crawlee.crawlers import PlaywrightCrawler

async def extract_table_data():
    crawler = PlaywrightCrawler(headless=True, browser_type='chromium')
    
    @crawler.router.default_handler
    async def request_handler(context):
        await context.page.wait_for_load_state('networkidle')
        
        # 等待表格加载
        await context.page.wait_for_selector('table', timeout=10000)
        
        # 获取表格数据
        rows = await context.page.query_selector_all('tr')
        for row in rows:
            cells = await row.query_selector_all('td, th')
            cell_texts = []
            for cell in cells:
                text = await cell.text_content()
                cell_texts.append(text.strip() if text else "")
            print(cell_texts)
    
    await crawler.run(['https://target-site.com'])

asyncio.run(extract_table_data())
```

## 已验证的测试结果

### 测试1：基本功能
- 测试站点：https://example.com
- 结果：✅ 成功
- 页面标题：Example Domain
- 页面内容长度：528 字符

### 测试2：SPA站点抓取
- 测试站点：https://github.com/trending
- 结果：✅ 成功
- 页面标题：Trending repositories on GitHub today · GitHub
- 页面内容长度：684,931 字符

### 测试3：artificialanalysis.ai
- 测试站点：https://artificialanalysis.ai
- 结果：⚠️ 被Vercel安全检查拦截
- 页面标题：Vercel Security Checkpoint
- 错误信息：无法验证您的浏览器

## 已知问题和解决方案

### 1. Vercel安全检查点
**问题**：artificialanalysis.ai等站点有Vercel安全检查，headless浏览器会被拦截

**解决方案**：
1. 使用crawlee的指纹伪装功能（需要额外配置）
2. 使用代理IP
3. 降级到API数据源（如OpenRouter API）

### 2. 导入错误
**问题**：`from crawlee.playwright_crawler import PlaywrightCrawler` 失败

**解决方案**：正确的导入方式是：
```python
from crawlee.crawlers import PlaywrightCrawler
```

### 3. 参数错误
**问题**：`use_fingerprint_cache` 参数不支持

**解决方案**：检查crawlee版本，使用正确的参数。当前版本（1.7.1）的PlaywrightCrawler支持的参数包括：
- headless: bool
- browser_type: str ('chromium', 'firefox', 'webkit')

## 依赖包版本（2026-05-31验证）
- crawlee: 1.7.1
- playwright: 1.60.0
- browserforge: 1.2.4
- greenlet: 3.5.1

## 参考链接
- Crawlee官方文档：https://crawlee.dev/
- Playwright官方文档：https://playwright.dev/
- Crawlee GitHub：https://github.com/apify/crawlee (⭐23,573)
