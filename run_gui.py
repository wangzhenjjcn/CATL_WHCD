#!/usr/bin/env python3
"""
ESP32S3 Sense 音频可视化器 - 快速启动脚本
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查依赖是否安装"""
    missing_deps = []
    
    try:
        import PyQt6
    except ImportError:
        missing_deps.append("PyQt6")
    
    try:
        import pyqtgraph
    except ImportError:
        missing_deps.append("pyqtgraph")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    if missing_deps:
        print(f"缺少依赖: {', '.join(missing_deps)}")
        return False
    return True

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("依赖安装失败，请手动运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("ESP32S3 Sense 音频可视化器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        print("检测到缺少依赖，正在安装...")
        if not install_dependencies():
            print("依赖安装失败，程序退出")
            return
    
    # 启动GUI程序
    print("启动GUI程序...")
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # 导入并运行主程序
        from app import main
        main()
    except Exception as e:
        print(f"启动失败: {e}")
        print("请检查src/app.py文件是否存在")

if __name__ == "__main__":
    main() 