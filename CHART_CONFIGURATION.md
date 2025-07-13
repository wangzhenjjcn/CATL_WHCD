# 图表配置说明

## 不同图表类型的坐标系统

### 1. 波形图 (Waveform)
**用途**: 显示时域音频信号
**坐标系统**:
- **X轴**: 时间 (线性)
- **Y轴**: 振幅 (线性)
- **范围**: -32768 到 32768 (16位音频)
- **单位**: 原始音频样本值

**特点**:
- 显示音频信号的时域变化
- 可以看到信号的幅度和形状
- 适合观察音频的动态变化

### 2. 频谱图 (Spectrum)
**用途**: 显示频域音频信号
**坐标系统**:
- **X轴**: 频率 (线性)
- **Y轴**: 幅度 (对数)
- **范围**: 0-8000Hz, -60dB到0dB
- **单位**: Hz, dB

**特点**:
- 显示音频信号的频率成分
- 使用对数坐标符合人耳特性
- 适合分析音频的频谱特征

### 3. 瀑布图 (Waterfall)
**用途**: 显示时频图
**坐标系统**:
- **X轴**: 时间 (线性)
- **Y轴**: 强度 (线性)
- **范围**: 0 到 32768
- **单位**: 信号强度

**特点**:
- 显示信号强度随时间的变化
- 使用RMS计算信号强度
- 适合观察音频的能量分布

## 坐标系统选择原理

### 波形图 - 线性坐标
```python
# 线性坐标适合时域显示
self.graph_widget.setLogMode(x=False, y=False)
self.graph_widget.setYRange(-32768, 32768)
```

**原因**:
- 时域信号通常有正负值
- 线性坐标直观显示信号幅度
- 便于观察信号的对称性

### 频谱图 - 对数坐标
```python
# 对数坐标适合频域显示
self.graph_widget.setLogMode(x=False, y=True)
self.graph_widget.setYRange(-60, 0)
```

**原因**:
- 人耳对声音的响应是对数的
- 可以同时显示强弱信号
- 符合音频分析的标准做法

### 瀑布图 - 线性坐标
```python
# 线性坐标适合强度显示
self.graph_widget.setLogMode(x=False, y=False)
self.graph_widget.setYRange(0, 32768)
```

**原因**:
- 强度值总是正值
- 线性坐标便于观察相对强度
- 适合观察信号的能量分布

## 数据处理策略

### 波形图数据处理
```python
# 限制显示点数，避免过于密集
if len(self.audio_data) > 1000:
    step = len(self.audio_data) // 1000
    x_data = x_data[::step]
    y_data = self.audio_data[::step]
```

### 频谱图数据处理
```python
# 使用窗函数和FFT
window = np.hanning(len(recent_data))
windowed_data = recent_data * window
fft_data = np.fft.fft(windowed_data)
```

### 瀑布图数据处理
```python
# 使用滑动窗口计算RMS
window_size = 64
intensity = []
for i in range(0, len(self.audio_data) - window_size, window_size):
    window_data = self.audio_data[i:i+window_size]
    rms = np.sqrt(np.mean(np.array(window_data) ** 2))
    intensity.append(rms)
```

## 性能优化

### 更新频率控制
- **波形图**: 20 FPS
- **频谱图**: 10 FPS (FFT计算较重)
- **瀑布图**: 15 FPS

### 数据缓冲区
- **波形图**: 1000点
- **频谱图**: 2048点 (FFT要求)
- **瀑布图**: 动态调整

### 内存管理
- 定期清理旧数据
- 限制最大数据点数
- 使用数据采样减少计算量

## 扩展建议

### 1. 添加更多图表类型
- **相位图**: 显示信号相位
- **相关性图**: 显示信号相关性
- **功率谱密度**: 更精确的频谱分析

### 2. 交互功能
- **缩放**: 支持鼠标缩放
- **平移**: 支持拖拽平移
- **标记**: 支持频率标记

### 3. 实时分析
- **峰值检测**: 自动检测频谱峰值
- **频率跟踪**: 跟踪主要频率成分
- **噪声分析**: 分析背景噪声水平 