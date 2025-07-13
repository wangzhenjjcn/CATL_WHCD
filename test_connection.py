#!/usr/bin/env python3
"""
ESP32S3连接测试脚本
"""

import socket
import json
import time

def test_connection(host='192.168.1.100', port=8080, timeout=5):
    """测试与ESP32S3的连接"""
    print(f"测试连接到 {host}:{port}")
    
    try:
        # 创建socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        print("✓ 连接成功!")
        
        # 接收数据
        print("等待数据...")
        buffer = ""
        start_time = time.time()
        
        while time.time() - start_time < 10:  # 测试10秒
            try:
                data = sock.recv(1024)
                if data:
                    buffer += data.decode('utf-8')
                    print(f"接收到 {len(data)} 字节数据")
                    
                    # 尝试解析JSON
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            try:
                                json_data = json.loads(line)
                                if 'audio_data' in json_data:
                                    audio_data = json_data['audio_data']
                                    print(f"✓ 成功解析JSON数据，音频数据长度: {len(audio_data)}")
                                    print(f"  数据范围: {min(audio_data)} 到 {max(audio_data)}")
                                    return True
                            except json.JSONDecodeError:
                                print(f"✗ JSON解析失败: {line[:50]}...")
                            except Exception as e:
                                print(f"✗ 数据处理错误: {e}")
                else:
                    print("连接已关闭")
                    break
                    
            except socket.timeout:
                print("接收数据超时")
                break
            except Exception as e:
                print(f"接收数据错误: {e}")
                break
                
    except socket.timeout:
        print("✗ 连接超时")
        return False
    except ConnectionRefusedError:
        print("✗ 连接被拒绝，请检查ESP32S3是否正在运行")
        return False
    except Exception as e:
        print(f"✗ 连接错误: {e}")
        return False
    finally:
        sock.close()
    
    return False

def main():
    """主函数"""
    print("ESP32S3 Sense 连接测试")
    print("=" * 30)
    
    # 测试默认IP
    if test_connection():
        print("\n✓ 连接测试成功!")
    else:
        print("\n✗ 连接测试失败!")
        print("\n请检查:")
        print("1. ESP32S3是否已上传程序")
        print("2. WiFi连接是否正常")
        print("3. IP地址是否正确")
        print("4. 防火墙设置")

if __name__ == "__main__":
    main() 