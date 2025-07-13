@echo off
chcp 65001 >nul
echo ESP32S3音频服务器 - 串口监控
echo ===============================

echo.
echo 正在连接到COM10端口...
echo 波特率: 115200
echo.
echo 按 Ctrl+C 退出监控
echo.

pio device monitor --port COM10 --baud 115200 