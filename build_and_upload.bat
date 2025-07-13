@echo off
chcp 65001 >nul
echo ESP32S3音频服务器 - 编译和上传脚本
echo ================================================

:: 检查PlatformIO是否安装
echo 检查PlatformIO...
pio --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: PlatformIO未安装
    echo 请先安装PlatformIO Core: pip install platformio
    pause
    exit /b 1
)

:: 进入项目目录
cd esp32s3_audio_server

:: 安装ArduinoJson库
echo.
echo 安装ArduinoJson库...
pio lib install "bblanchon/ArduinoJson@^6.21.3"

:: 编译项目
echo.
echo 编译ESP32S3程序...
pio run

if errorlevel 1 (
    echo ❌ 编译失败
    pause
    exit /b 1
)

echo ✅ 编译成功!

:: 询问是否上传
echo.
set /p upload="是否上传到ESP32S3设备? (y/n): "
if /i "%upload%"=="y" (
    echo.
    echo 上传程序到ESP32S3...
    pio run --target upload
    
    if errorlevel 1 (
        echo ❌ 上传失败
        echo 请检查设备连接和COM端口
    ) else (
        echo ✅ 上传成功!
    )
)

echo.
echo 完成!
pause 