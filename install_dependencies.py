#!/usr/bin/env python3
"""
安装Python依赖脚本
"""

import subprocess
import sys
import os

def install_requirements():
    """安装requirements.txt中的依赖"""
    print("正在安装Python依赖...")
    
    try:
        # 检查pip是否可用
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("错误: pip不可用")
        return False
    
    try:
        # 安装依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败: {e}")
        return False

def check_pyqt6():
    """检查PyQt6是否正确安装"""
    try:
        import PyQt6
        print("PyQt6 已安装")
        return True
    except ImportError:
        print("PyQt6 未安装")
        return False

def check_pyqtgraph():
    """检查pyqtgraph是否正确安装"""
    try:
        import pyqtgraph
        print("pyqtgraph 已安装")
        return True
    except ImportError:
        print("pyqtgraph 未安装")
        return False

def main():
    """主函数"""
    print("ESP32S3 Sense 音频可视化器 - 依赖安装")
    print("=" * 50)
    
    # 安装依赖
    if install_requirements():
        print("\n检查关键依赖...")
        
        if check_pyqt6() and check_pyqtgraph():
            print("\n所有依赖安装成功!")
            print("现在可以运行: python src/app.py")
        else:
            print("\n某些依赖安装失败，请手动安装:")
            print("pip install PyQt6 pyqtgraph numpy")
    else:
        print("\n依赖安装失败，请检查网络连接或手动安装")

if __name__ == "__main__":
    main() 