# ESP32S3 Sense 音频可视化器

这是一个基于Qt6的GUI应用程序，用于实时显示Seeed Studio XIAO ESP32S3 Sense的音频数据。

## 功能特性

- 实时音频波形显示
- WiFi连接ESP32S3设备
- 可调节显示参数
- 数据统计信息
- 支持多种图表类型

## 硬件要求

- Seeed Studio XIAO ESP32S3 Sense
- USB数据线
- 电脑（Windows/Linux/macOS）

## 软件要求

### 电脑端
- Python 3.8+
- PyQt6
- pyqtgraph
- numpy

### 设备端
- Arduino IDE 或 PlatformIO
- ESP32开发板支持
- ArduinoJson库

## 安装步骤

### 1. 安装Python依赖

```bash
# 运行安装脚本
python install_dependencies.py

# 或手动安装
pip install -r requirements.txt
```

### 2. 配置ESP32S3设备

#### 方法一：使用Arduino IDE

1. 打开Arduino IDE
2. 安装ESP32开发板支持
3. 安装ArduinoJson库
4. 打开`esp32s3_audio_server.ino`文件
5. 选择正确的开发板和端口
6. 上传代码到设备

#### 方法二：使用PlatformIO

1. 安装PlatformIO
2. 在项目根目录运行：
   ```bash
   pio run --target upload
   ```

### 3. 配置WiFi

在`esp32s3_audio_server.ino`中修改WiFi配置：

```cpp
const char* ssid = "你的WiFi名称";
const char* password = "你的WiFi密码";
```

## 使用方法

### 1. 启动设备

1. 将ESP32S3连接到电脑
2. 上传代码到设备
3. 打开串口监视器查看连接状态
4. 记录设备的IP地址

### 2. 启动GUI程序

```bash
python src/app.py
```

### 3. 连接设备

1. 在GUI中输入设备的IP地址（默认192.168.1.100）
2. 端口号保持8080
3. 点击"连接"按钮
4. 观察连接状态和数据显示

## 程序结构

```
CATL_WHCD/
├── src/
│   └── app.py              # Qt6 GUI主程序
├── esp32s3_audio_server.ino # ESP32S3设备端程序
├── requirements.txt         # Python依赖
├── platformio.ini          # PlatformIO配置
├── install_dependencies.py # 依赖安装脚本
└── README_ESP32S3_Audio.md # 使用说明
```

## 故障排除

### 常见问题

1. **无法连接到设备**
   - 检查WiFi连接
   - 确认IP地址正确
   - 检查防火墙设置

2. **没有音频数据**
   - 检查I2S麦克风连接
   - 确认代码正确上传
   - 查看串口监视器输出

3. **GUI程序无法启动**
   - 检查Python依赖安装
   - 确认PyQt6和pyqtgraph已安装

### 调试步骤

1. 打开串口监视器查看设备状态
2. 检查WiFi连接是否成功
3. 确认服务器是否启动
4. 测试网络连接（ping设备IP）

## 技术细节

### 数据格式

设备发送JSON格式的音频数据：

```json
{
  "audio_data": [1024, 2048, 1536, ...]
}
```

### 采样参数

- 采样率：16kHz
- 位深度：16位
- 缓冲区大小：1024样本
- 传输频率：约100Hz

### 网络配置

- 协议：TCP
- 端口：8080
- 数据格式：JSON

## 扩展功能

### 可添加的功能

1. 频谱分析
2. 音频录制
3. 音量控制
4. 多设备支持
5. 数据保存

### 代码修改建议

1. 修改采样率：更改`sample_rate`参数
2. 调整缓冲区大小：修改`BUFFER_SIZE`
3. 添加音频处理：在`sendAudioData()`中添加滤波
4. 实现频谱显示：使用FFT算法

## 许可证

本项目基于MIT许可证开源。

## 联系方式

如有问题，请查看项目文档或提交Issue。 