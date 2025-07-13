# ESP32S3程序上传指南

## 问题解决

您遇到的错误 `Wrong boot mode detected (0x29)! The chip needs to be in download mode.` 表示ESP32S3需要进入下载模式。

## 解决方案

### 方法1: 手动进入下载模式

1. **按住BOOT按钮** - 在ESP32S3 XIAO Sense开发板上找到BOOT按钮
2. **保持按住BOOT按钮的同时，按一下RESET按钮**
3. **松开RESET按钮，但继续按住BOOT按钮**
4. **运行上传命令**：
   ```bash
   pio run --target upload
   ```
5. **看到"Connecting..."开始时，松开BOOT按钮**

### 方法2: 使用自动重置

如果手动方法不起作用，可以尝试：

1. **断开USB连接**
2. **按住BOOT按钮**
3. **插入USB连接**
4. **运行上传命令**
5. **松开BOOT按钮**

### 方法3: 修改上传配置

在platformio.ini中添加上传配置：

```ini
[env:seeed_xiao_esp32s3]
platform = espressif32
board = seeed_xiao_esp32s3
framework = arduino
monitor_speed = 115200
lib_deps = 
    bblanchon/ArduinoJson @ ^6.21.3
build_flags = 
    -DCORE_DEBUG_LEVEL=3
    -DARDUINO_USB_CDC_ON_BOOT=1
upload_speed = 460800
monitor_port = COM10
upload_port = COM10
```

## 完整上传流程

1. **编译程序**：
   ```bash
   pio run
   ```

2. **进入下载模式**：
   - 按住BOOT按钮
   - 按一下RESET按钮
   - 松开RESET按钮，继续按住BOOT按钮

3. **上传程序**：
   ```bash
   pio run --target upload
   ```

4. **松开BOOT按钮**

5. **监控串口输出**：
   ```bash
   pio device monitor
   ```

## 验证上传成功

上传成功后，您应该在串口监视器中看到：

```
连接到WiFi: 1500M
.....
WiFi连接成功!
IP地址: 192.168.0.194
网关: 192.168.0.1
子网掩码: 255.255.255.0
I2S麦克风初始化完成
服务器已启动，端口: 8080
```

## 故障排除

### 常见问题

1. **仍然无法连接**
   - 检查USB线缆是否正常
   - 尝试不同的USB端口
   - 确认设备管理器中显示COM10

2. **上传后没有输出**
   - 按一下RESET按钮重启设备
   - 检查串口监视器的波特率设置（115200）

3. **WiFi连接失败**
   - 检查WiFi密码是否正确
   - 确认设备在WiFi信号范围内
   - 检查路由器是否允许新设备连接

### 调试命令

```bash
# 查看详细上传日志
pio run --target upload --verbose

# 监控串口输出
pio device monitor --port COM10 --baud 115200

# 强制指定端口上传
pio run --target upload --upload-port COM10
```

## 下一步

上传成功后，您可以：

1. **运行GUI程序**：
   ```bash
   cd ..
   python run_gui.py
   ```

2. **测试连接**：
   ```bash
   python test_connection.py
   ```

3. **查看设备IP地址**，然后在GUI程序中输入该IP地址进行连接。 