# ESP32S3音频服务器编译指南

## 问题解决

您遇到的 `ArduinoJson.h: No such file or directory` 错误是因为缺少ArduinoJson库。以下是解决方案：

## 解决方案

### 方案1: 使用完整版本（推荐）

1. **安装ArduinoJson库**
   ```bash
   cd esp32s3_audio_server
   pio lib install "bblanchon/ArduinoJson@^6.21.3"
   ```

2. **编译程序**
   ```bash
   pio run
   ```

3. **上传到设备**
   ```bash
   pio run --target upload
   ```

### 方案2: 使用简化版本

如果ArduinoJson库安装有问题，可以使用简化版本：

1. **重命名配置文件**
   ```bash
   cd esp32s3_audio_server
   ren platformio.ini platformio_full.ini
   copy platformio_simple.ini platformio.ini
   ```

2. **使用简化程序**
   ```bash
   copy esp32s3_audio_server_simple.ino esp32s3_audio_server.ino
   ```

3. **编译和上传**
   ```bash
   pio run
   pio run --target upload
   ```

### 方案3: 使用批处理脚本

直接运行提供的批处理脚本：
```bash
build_and_upload.bat
```

## 文件说明

### 主要文件
- `esp32s3_audio_server.ino` - 完整版本（需要ArduinoJson）
- `esp32s3_audio_server_simple.ino` - 简化版本（无需ArduinoJson）
- `platformio.ini` - 完整配置（包含ArduinoJson依赖）
- `platformio_simple.ini` - 简化配置（无ArduinoJson依赖）

### 配置文件
- `platformio.ini` - PlatformIO项目配置
- `build_and_upload.bat` - Windows编译上传脚本
- `install_arduinojson.py` - ArduinoJson安装脚本

## 数据格式

### 完整版本（JSON格式）
```json
{
  "audio_data": [1234, 5678, -1234, ...]
}
```

### 简化版本（CSV格式）
```
1234,5678,-1234,...
```

## 故障排除

### 常见问题

1. **PlatformIO未安装**
   ```bash
   pip install platformio
   ```

2. **ArduinoJson库安装失败**
   - 使用简化版本
   - 检查网络连接
   - 尝试手动下载库文件

3. **编译错误**
   - 检查ESP32S3开发板配置
   - 确认引脚定义正确
   - 检查WiFi配置

4. **上传失败**
   - 检查USB连接
   - 确认COM端口正确
   - 按住BOOT按钮再上传

### 调试步骤

1. **检查串口输出**
   ```bash
   pio device monitor
   ```

2. **查看编译日志**
   ```bash
   pio run --verbose
   ```

3. **测试WiFi连接**
   - 检查WiFi密码是否正确
   - 确认设备在WiFi范围内

## 引脚配置

ESP32S3 XIAO Sense I2S引脚：
- WS (Word Select): GPIO 15
- SD (Serial Data): GPIO 13  
- SCK (Serial Clock): GPIO 2

## 网络配置

- WiFi SSID: `1500M`
- WiFi密码: `23457890`
- 服务器端口: `8080`

## 测试连接

上传成功后，设备会：
1. 连接WiFi网络
2. 启动TCP服务器
3. 开始采集音频数据
4. 等待客户端连接

可以通过串口监视器查看连接状态和IP地址。 