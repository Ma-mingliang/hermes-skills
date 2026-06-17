# 微信小程序数据记录功能

## 实现日期
2026-05-30

## 功能说明
微信小程序新增数据记录功能，可以记录遥测数据并导出为CSV文件，用于后续数据分析。

## 修改文件
1. `bike/wx/pages/index/index.js` - 添加数据记录、导出CSV功能
2. `bike/wx/pages/index/index.wxml` - 添加记录控制按钮和状态显示
3. `bike/wx.md` - 添加数据记录功能说明

## 实现要点

### 数据记录
```javascript
// 在onNotify中记录数据
recordData(modeId, roll, pitch, batt) {
  if (!this.data.recording) return;
  
  this.dataRecords.push({
    timestamp: Date.now(),
    modeId,
    roll,
    pitch,
    batt
  });
  
  // 限制记录数量
  if (this.dataRecords.length > this.data.maxRecordCount) {
    this.dataRecords.shift();
  }
  
  this.setData({ recordCount: this.dataRecords.length });
}
```

### CSV导出
```javascript
exportData() {
  let csv = 'timestamp,modeId,roll,pitch,batt\n';
  this.dataRecords.forEach(record => {
    csv += `${record.timestamp},${record.modeId},${record.roll},${record.pitch},${record.batt}\n`;
  });
  
  const fs = wx.getFileSystemManager();
  const filePath = `${wx.env.USER_DATA_PATH}/bike_data_${Date.now()}.csv`;
  fs.writeFile({
    filePath,
    data: csv,
    encoding: 'utf8',
    success: () => {
      // 分享文件
      wx.shareFileMessage({ filePath });
    }
  });
}
```

### UI控件
- 开始/停止记录按钮
- 清空记录按钮
- 导出CSV按钮
- 记录状态和数量显示

## 数据格式

CSV文件包含以下字段：
- `timestamp` - 时间戳（毫秒）
- `modeId` - 模式ID（0=Idle, 1=Segway, 2=Bike）
- `roll` - 横滚角（度）
- `pitch` - 俯仰角（度）
- `batt` - 电池电压（V）

## 使用流程

1. 打开微信小程序
2. 连接到BikeESP32
3. 点击"开始记录"按钮
4. 进行测试（切换模式、调整参数等）
5. 点击"停止记录"按钮
6. 点击"导出CSV"按钮
7. 通过微信分享将CSV文件保存到电脑

## Python数据分析

分析脚本：`tools/analyze_data.py`

```bash
# 安装依赖
pip install pandas matplotlib numpy

# 分析数据
python tools/analyze_data.py bike_data.csv

# 指定输出目录
python tools/analyze_data.py bike_data.csv -o my_analysis
```

分析结果：
- 响应曲线图（俯仰角、横滚角、电池电压）
- 性能指标（均值、标准差、稳态误差、调节时间、超调量）
- 按模式分析
- 分析摘要文件

## 调试信息

调试帧中包含的字段：
- `pitchDeg` - 俯仰角
- `pitchRateDeg` - 俯仰角速度
- `actualSpeed` - 实际速度
- `speedOutput` - 速度环输出
- `targetAngle` - 目标角度
- `balanceOutput` - 直立环输出
- `speedIntegral` - 速度环积分项
