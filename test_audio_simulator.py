#!/usr/bin/env python3
"""
音频数据模拟器 - 用于测试GUI程序
"""

import socket
import json
import time
import math
import threading
import random

class AudioSimulator:
    """音频数据模拟器"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.frequency = 440  # 440Hz正弦波
        self.sample_rate = 16000
        self.amplitude = 1000
        
    def start_server(self):
        """启动模拟服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            print(f"模拟服务器启动在 {self.host}:{self.port}")
            print("等待客户端连接...")
            
            self.running = True
            
            while self.running:
                client_socket, address = self.server_socket.accept()
                print(f"客户端连接: {address}")
                
                # 在新线程中处理客户端
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"服务器错误: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_client(self, client_socket):
        """处理客户端连接"""
        try:
            start_time = time.time()
            
            while self.running:
                # 生成模拟音频数据
                audio_data = self.generate_audio_data()
                
                # 创建JSON数据
                json_data = {
                    "audio_data": audio_data
                }
                
                # 发送数据
                message = json.dumps(json_data) + "\n"
                client_socket.send(message.encode('utf-8'))
                
                # 控制发送频率
                time.sleep(0.01)  # 100Hz
                
        except Exception as e:
            print(f"客户端处理错误: {e}")
        finally:
            client_socket.close()
    
    def generate_audio_data(self):
        """生成模拟音频数据"""
        data = []
        current_time = time.time()
        
        for i in range(1024):
            # 生成正弦波 + 噪声
            t = current_time + i / self.sample_rate
            sine_wave = self.amplitude * math.sin(2 * math.pi * self.frequency * t)
            noise = random.uniform(-100, 100)
            sample = int(sine_wave + noise)
            data.append(sample)
        
        return data
    
    def stop_server(self):
        """停止服务器"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()

def main():
    """主函数"""
    print("ESP32S3 Sense 音频数据模拟器")
    print("=" * 40)
    
    simulator = AudioSimulator()
    
    try:
        simulator.start_server()
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        simulator.stop_server()

if __name__ == "__main__":
    main() 