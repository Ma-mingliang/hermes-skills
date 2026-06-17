---
name: wechat-miniprogram-dev
description: 微信小程序开发工作流 — 工具安装、项目结构、JS语法陷阱、预览调试、BLE集成。适用于所有微信小程序开发场景。
triggers:
  - 微信小程序
  - 微信开发者工具
  - WeChat Mini Program
  - 小程序开发
  - 微信BLE
---

# 微信小程序开发

## 1. 安装微信开发者工具

### Windows安装
1. **winget安装**（推荐，但需管理员权限）:
   ```bash
   winget install Tencent.WeixinDevTools --accept-package-agreements --accept-source-agreements
   ```
   注意：winget安装需要管理员权限，普通用户会报 `[WinError 740] 请求的操作需要提升`

2. **手动下载**:
   - 访问 https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
   - 下载链接是JavaScript动态生成的，需用browser_console提取：
   ```javascript
   Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('download') || h.includes('.exe'))
   ```
   - 稳定版下载URL模式: `https://servicewechat.com/wxa-dev-logic/download_redirect?type=win32_x64&from=mpwiki&download_version={版本号}&version_type=1`

3. **安装路径**:
   - 默认: `C:\Program Files (x86)\Tencent\微信web开发者工具`
   - 用户自定义: 搜索 `D:\微信web开发者工具` 等路径
   - 可执行文件: `微信开发者工具.exe` 或 `wechatdevtools.exe`

### macOS安装
- 下载darwin_x64或darwin_arm64版本
- 拖拽到Applications目录

## 2. 项目结构

```
wx/
├── app.js              # 小程序入口
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── project.config.json # 项目配置
├── sitemap.json        # 站点地图
└── pages/
    └── index/
        ├── index.js    # 页面逻辑
        ├── index.wxml  # 页面模板
        ├── index.wxss  # 页面样式
        └── index.json  # 页面配置
```

## 3. JS语法陷阱（高频错误）

### ❌ 单引号字符串不能跨行
```javascript
// 错误！Unterminated string constant
let csv = 'timestamp,modeId,roll,pitch,batt
';

// 正确：使用 \n
let csv = 'timestamp,modeId,roll,pitch,batt\n';

// 或使用模板字符串
let csv = `timestamp,modeId,roll,pitch,batt
`;
```

### ❌ 模板字符串中换行也要注意
```javascript
// 错误！
csv += `${record.timestamp},${record.modeId}
`;

// 正确
csv += `${record.timestamp},${record.modeId}\n`;
```

### ✅ CSV生成最佳实践
```javascript
const headers = ['timestamp', 'modeId', 'roll', 'pitch', 'batt'];
let csv = headers.join(',') + '\n';

this.dataRecords.forEach(record => {
  csv += `${record.timestamp},${record.modeId},${record.roll},${record.pitch},${record.batt}\n`;
});
```

## 4. 预览与调试

### 预览流程
1. 微信开发者工具 → 点击"预览"按钮
2. 用iPhone微信扫描二维码
3. 在手机上测试

### 真机调试
1. 点击"真机调试"按钮
2. 可在电脑上查看日志
3. 支持断点调试

### 常见预览错误
- **JS语法错误**: 检查控制台错误信息，定位到具体行号
- **组件未找到**: 检查app.json中的pages配置
- **BLE连接失败**: 检查iPhone蓝牙权限设置

## 5. BLE蓝牙集成

### 权限配置
在 `app.json` 中添加：
```json
{
  "permissions": {
    "scope.bluetooth": {
      "desc": "用于连接自行车控制设备"
    }
  }
}
```

### BLE API
```javascript
// 扫描设备
wx.openBluetoothAdapter()
wx.startBluetoothDevicesDiscovery()

// 连接设备
wx.createBLEConnection({ deviceId })

// 读取数据
wx.notifyBLECharacteristicValueChange()
wx.onBLECharacteristicValueChange(callback)
```

## 6. iOS特殊注意

| 项目 | iOS要求 | 备注 |
|------|---------|------|
| 微信版本 | >= 7.0 | 必须 |
| 系统版本 | iOS 9.0+ | 必须 |
| BLE蓝牙 | 需要授权 | 首次使用需授权 |
| 文件导出 | 使用微信分享 | 不是直接下载 |
| 后台运行 | 受限 | 需保持小程序在前台 |

## 7. 实时数据图表 (Canvas)

### WXML
```xml
<view class="chart-container">
  <canvas canvas-id="dataChart" id="dataChart" class="data-chart"></canvas>
</view>
```

### JS初始化与更新
```javascript
initChart() {
  const ctx = wx.createCanvasContext('dataChart', this);
  this.chartCtx = ctx;
  this.drawChart();
},

updateChartData(record) {
  const maxPoints = 50;
  this.chartData.pitch.push(record.pitch);
  if (this.chartData.pitch.length > maxPoints) this.chartData.pitch.shift();
  this.drawChart();
},

drawChart() {
  const ctx = this.chartCtx;
  ctx.clearRect(0, 0, width, height);
  // 绘制网格线、数据线
  ctx.draw();
}
```

**Pitfall**: Canvas容器必须设置明确的width/height，否则不显示。

## 8. 参数调整UI (PID等)

### WXML模式
```xml
<view class="pid-row">
  <text class="pid-label">Kp:</text>
  <input class="pid-input" type="digit" value="{{pidParams.pitch_kp}}" 
         bindinput="onPitchKpInput"/>
  <button class="pid-btn" bindtap="sendPitchKp">发送</button>
</view>
```

### JS模式
```javascript
onPitchKpInput(e) {
  this.setData({ 'pidParams.pitch_kp': parseFloat(e.detail.value) || 0 });
},
sendPitchKp() {
  this.setPidParam('P_KP', this.data.pidParams.pitch_kp);
},
setPidParam(paramId, value) {
  this.sendBleCommand(`PID:${paramId}:${value}`);
},
```

## 9. 本地历史数据管理

### 保存到本地存储
```javascript
saveDataToStorage() {
  let history = wx.getStorageSync('bike_history') || [];
  history.unshift({ timestamp: Date.now(), records: this.data.dataRecords, count: this.data.dataRecords.length });
  if (history.length > 10) history = history.slice(0, 10);
  wx.setStorageSync('bike_history', history);
},
```

### 加载和展示
```javascript
loadHistoryData() {
  this.setData({ historyData: wx.getStorageSync('bike_history') || [] });
},
```

**Pitfall**: wx.setStorageSync有大小限制，大数据集应限制存储条数（建议10条以内）。

## 10. 错误处理增强

### 用户友好错误提示
```javascript
setError(err) {
  const s = typeof err === 'string' ? err : (err.errMsg || JSON.stringify(err));
  let userMessage = '操作失败';
  if (s.includes('蓝牙')) userMessage = '蓝牙连接失败，请检查设备';
  else if (s.includes('超时')) userMessage = '连接超时，请重试';
  wx.showToast({ title: userMessage, icon: 'none' });
},
```

### BLE连接带重试
```javascript
fail: (e) => {
  this.hideLoading();
  this.setError(e);
  wx.showModal({
    title: '连接失败', content: '是否重试？',
    success: (res) => { if (res.confirm) this.connectDevice(deviceId); }
  });
}
```

## 11. 工作流检查清单

- [ ] 微信开发者工具已安装
- [ ] 项目路径正确（检查app.json）
- [ ] JS语法无错误（检查控制台）
- [ ] BLE权限已配置
- [ ] 预览二维码可扫描
- [ ] iOS设备已授权蓝牙

## Pitfalls

1. **安装路径不在C盘**: 用户可能自定义安装到D盘，搜索时需检查多个盘符
2. **winget需要管理员权限**: 普通用户会失败，需提示用户以管理员运行
3. **下载链接动态生成**: 微信开发者工具下载页面的链接是JS动态生成的，curl直接获取页面拿不到
4. **单引号跨行**: 这是最常见的JS语法错误，微信开发者工具会报 "Unterminated string constant"
5. **iOS后台BLE限制**: iOS限制后台BLE通信，需保持小程序在前台
6. **CSV导出**: iOS通过微信分享保存，不是直接下载文件
7. **Canvas不显示**: 容器必须设置明确的width/height
8. **本地存储溢出**: wx.setStorageSync有大小限制，历史数据需限制条数

## References

- `references/installation-windows.md` — Windows安装详细步骤和URL模式
- `references/data-analysis-python.md` — Python数据分析工具模式（FFT、相关性、对比、报告生成）
