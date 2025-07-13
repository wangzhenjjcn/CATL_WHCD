#!/usr/bin/env python3
"""
ArduinoJson库安装脚本
用于在PlatformIO项目中安装ArduinoJson库
"""

import os
import subprocess
import sys

def install_arduinojson():
    """安装ArduinoJson库"""
    print("正在安装ArduinoJson库...")
    
    try:
        # 使用PlatformIO安装ArduinoJson库
        cmd = ["pio", "lib", "install", "bblanchon/ArduinoJson@^6.21.3"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd="esp32s3_audio_server")
        
        if result.returncode == 0:
            print("✅ ArduinoJson库安装成功!")
            print(result.stdout)
        else:
            print("❌ ArduinoJson库安装失败:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ 错误: 未找到PlatformIO命令")
        print("请确保已安装PlatformIO Core")
        return False
    except Exception as e:
        print(f"❌ 安装过程中出现错误: {e}")
        return False
    
    return True

def check_platformio():
    """检查PlatformIO是否已安装"""
    try:
        result = subprocess.run(["pio", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PlatformIO已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ PlatformIO未正确安装")
            return False
    except FileNotFoundError:
        print("❌ PlatformIO未安装")
        return False

def main():
    """主函数"""
    print("ESP32S3音频服务器 - ArduinoJson库安装工具")
    print("=" * 50)
    
    # 检查PlatformIO
    if not check_platformio():
        print("\n请先安装PlatformIO Core:")
        print("pip install platformio")
        return
    
    # 检查项目目录
    if not os.path.exists("esp32s3_audio_server"):
        print("❌ 错误: 未找到esp32s3_audio_server目录")
        return
    
    # 安装ArduinoJson库
    if install_arduinojson():
        print("\n🎉 安装完成!")
        print("\n现在您可以编译ESP32S3程序:")
        print("cd esp32s3_audio_server")
        print("pio run")
    else:
        print("\n❌ 安装失败，请检查错误信息")

if __name__ == "__main__":
    main() 