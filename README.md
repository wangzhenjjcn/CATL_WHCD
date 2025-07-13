# CATL_WHCD
Wire harness connection detection for CATL

## ESP32S3 Sense 音频可视化器

本项目包含一个基于Qt6的GUI应用程序，用于实时显示Seeed Studio XIAO ESP32S3 Sense的音频数据。

### 快速开始

1. **安装依赖**
   ```bash
   python install_dependencies.py
   ```

2. **测试连接**
   ```bash
   python test_connection.py
   ```

3. **启动GUI程序**
   ```bash
   # 完整版 (需要pyqtgraph)
   python src/app.py
   
   # 简化版 (仅需PyQt6)
   python src/simple_app.py
   
   # 或使用启动脚本
   start_gui.bat
   ```

4. **测试程序**
   ```bash
   python test_audio_simulator.py
   ```

### 文件结构

- `src/app.py` - Qt6 GUI主程序 (完整版)
- `src/simple_app.py` - Qt6 GUI主程序 (简化版)
- `esp32s3_audio_server.ino` - ESP32S3设备端程序
- `requirements.txt` - Python依赖
- `platformio.ini` - PlatformIO配置
- `test_audio_simulator.py` - 音频数据模拟器
- `test_connection.py` - 连接测试脚本
- `start_gui.bat` - Windows启动脚本
- `README_ESP32S3_Audio.md` - 详细使用说明

### 硬件要求

- Seeed Studio XIAO ESP32S3 Sense
- USB数据线
- WiFi网络

### 软件要求

- Python 3.8+
- PyQt6
- pyqtgraph
- Arduino IDE 或 PlatformIO

### 故障排除

#### 常见问题

1. **套接字错误**
   - 确保ESP32S3已正确连接WiFi
   - 检查IP地址是否正确
   - 运行 `python test_connection.py` 测试连接

2. **图表切换无效**
   - 确保有音频数据正在接收
   - 尝试使用简化版程序：`python src/simple_app.py`
   - 检查控制台输出是否有错误信息

3. **依赖问题**
   - 运行 `python install_dependencies.py` 重新安装依赖
   - 使用简化版程序避免pyqtgraph依赖问题

#### 测试步骤

1. **连接测试**：
   ```bash
   python test_connection.py
   ```

2. **GUI测试**：
   ```bash
   python test_gui.py
   ```

3. **音频模拟器测试**：
   ```bash
   python test_audio_simulator.py
   ```

### 频谱图特性

- **频率范围**: 0 - 100,000 Hz (0-100kHz)
- **Y轴单位**: dB (分贝)，对数坐标
- **X轴单位**: Hz (赫兹)，线性坐标
- **FFT点数**: 2048点，提供7.8Hz分辨率
- **窗函数**: 汉宁窗，减少频谱泄漏

详细使用说明请参考 [README_ESP32S3_Audio.md](README_ESP32S3_Audio.md)
频谱分析技术说明请参考 [SPECTRUM_ANALYSIS.md](SPECTRUM_ANALYSIS.md)
