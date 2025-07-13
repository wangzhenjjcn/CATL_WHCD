@echo off
chcp 65001 >nul
echo ESP32S3音频服务器 - 快速上传脚本
echo ==========================================

echo.
echo 请按照以下步骤操作：
echo 1. 按住ESP32S3开发板上的BOOT按钮
echo 2. 保持按住BOOT按钮的同时，按一下RESET按钮
echo 3. 松开RESET按钮，但继续按住BOOT按钮
echo 4. 按任意键开始上传...
pause >nul

echo.
echo 正在上传程序...
echo （看到"Connecting..."时请松开BOOT按钮）
echo.

pio run --target upload

if errorlevel 1 (
    echo.
    echo ❌ 上传失败！
    echo 请检查：
    echo - 是否正确进入下载模式
    echo - USB连接是否正常
    echo - COM端口是否正确
    echo.
    echo 尝试重新运行此脚本
) else (
    echo.
    echo ✅ 上传成功！
    echo.
    echo 现在可以监控串口输出：
    echo pio device monitor
    echo.
    echo 或者运行GUI程序：
    echo cd ..
    echo python run_gui.py
)

echo.
pause 