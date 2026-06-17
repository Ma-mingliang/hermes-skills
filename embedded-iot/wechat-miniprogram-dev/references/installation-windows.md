# Windows安装微信开发者工具详细步骤

## 方法1: winget安装（推荐）

```bash
winget search 微信开发者工具
winget install Tencent.WeixinDevTools --accept-package-agreements --accept-source-agreements
```

**注意**:
- 需要管理员权限，否则报 `[WinError 740] 请求的操作需要提升`
- 如果有多个匹配（msstore和winget），需指定完整ID: `Tencent.WeixinDevTools`

## 方法2: 手动下载

### 获取下载URL
页面下载链接是JavaScript动态生成的，需用browser_console提取：

```javascript
Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('download') || h.includes('.exe'))
```

### 已知有效URL模式
- 稳定版: `https://servicewechat.com/wxa-dev-logic/download_redirect?type=win32_x64&from=mpwiki&download_version={版本号}&version_type=1`
- 开发版: `https://devtools.wxqcloud.qq.com.cn/WechatWebDev/nightly/electron-36.6.0/wechat_devtools_{版本号}_win32_x64.exe`
- 旧版: `https://dldir1.qq.com/WechatWebDev/nightly/p-{hash}/0.54.1/wechat_devtools_{版本号}_win32_x64.exe`

### 下载命令
```bash
curl -L -o wechat_devtools.exe "https://servicewechat.com/wxa-dev-logic/download_redirect?type=win32_x64&from=mpwiki&download_version=2012510290&version_type=1"
```

### 安装
```bash
# 静默安装（需要管理员权限）
wechat_devtools.exe /S

# 或手动双击安装
```

## 安装路径检测

常见安装路径：
```python
paths = [
    "C:/Program Files (x86)/Tencent/微信web开发者工具",
    "C:/Program Files/Tencent/微信web开发者工具",
    "D:/微信web开发者工具",
    "D:/Program Files (x86)/Tencent/微信web开发者工具",
    "C:/Users/{username}/AppData/Local/微信web开发者工具",
]
```

可执行文件名：
- `微信开发者工具.exe`
- `wechatdevtools.exe`

## 版本信息

| 版本类型 | 版本号 | 日期 | 备注 |
|---------|--------|------|------|
| 稳定版 | 2.01.2510290 | 2026/03/25 | 推荐 |
| 预发布版 | 2.01.2510241 | 2025/10/24 | 包含新特性 |
| 开发版(Electron) | 2.02.2605292 | 2026/05/29 | 基于Electron 36.6 |
| 开发版(NWJS) | 2.01.2602282 | 2026/02/28 | 基于NW.js 0.54.1 |
| 历史版 | 1.05.2204250 | - | 最后支持Win7 |

## 常见问题

1. **winget安装失败**: 需要管理员权限，以管理员运行终端
2. **下载链接404**: URL可能过期，需重新从页面提取
3. **安装后找不到**: 检查D盘自定义路径
4. **启动慢**: 首次启动需要初始化，等待10-30秒
