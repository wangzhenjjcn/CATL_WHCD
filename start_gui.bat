@echo off
echo ESP32S3 Sense 音频可视化器
echo ================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python未安装或不在PATH中
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

REM 选择版本
echo.
echo 请选择版本:
echo 1. 完整版 (需要pyqtgraph)
echo 2. 简化版 (仅需PyQt6)
echo.
set /p choice="请输入选择 (1 或 2): "

if "%choice%"=="1" (
    echo 启动完整版...
    python -c "import pyqtgraph" >nul 2>&1
    if errorlevel 1 (
        echo 警告: pyqtgraph未安装，将使用简化版
        python src/simple_app.py
    ) else (
        python src/app.py
    )
) else if "%choice%"=="2" (
    echo 启动简化版...
    python src/simple_app.py
) else (
    echo 无效选择，启动简化版...
    python src/simple_app.py
)

pause 