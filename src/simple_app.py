import sys
import json
import socket
import threading
import time
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QTextEdit, QGroupBox,
                             QGridLayout, QSpinBox, QComboBox, QProgressBar)
from PyQt6.QtCore import QTimer, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class DataReceiver(QObject):
    """数据接收器类，用于从ESP32S3接收数据"""
    data_received = pyqtSignal(list)
    connection_status = pyqtSignal(bool, str)
    
    def __init__(self, host='192.168.1.100', port=8080):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        self.buffer = ""  # 用于存储不完整的JSON数据
        
    def connect_to_device(self):
        """连接到ESP32S3设备"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.connection_status.emit(True, f"已连接到 {self.host}:{self.port}")
            return True
        except Exception as e:
            self.connected = False
            self.connection_status.emit(False, f"连接失败: {str(e)}")
            return False
    
    def disconnect_from_device(self):
        """断开与设备的连接"""
        self.running = False
        if self.socket:
            self.socket.close()
        self.connected = False
        self.connection_status.emit(False, "已断开连接")
    
    def start_receiving(self):
        """开始接收数据"""
        if not self.connected:
            return
            
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def _receive_data(self):
        """接收数据的线程函数"""
        while self.running and self.connected and self.socket:
            try:
                data = self.socket.recv(1024)
                if data:
                    # 将接收到的数据添加到缓冲区
                    self.buffer += data.decode('utf-8')
                    
                    # 查找完整的JSON消息（以换行符分隔）
                    while '\n' in self.buffer:
                        line, self.buffer = self.buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            try:
                                # 尝试解析JSON数据
                                json_data = json.loads(line)
                                if 'audio_data' in json_data:
                                    audio_data = json_data['audio_data']
                                    self.data_received.emit(audio_data)
                            except json.JSONDecodeError:
                                # 如果不是JSON，尝试解析为音频数据
                                try:
                                    audio_data = [int(x) for x in line.split(',') if x.strip()]
                                    if audio_data:
                                        self.data_received.emit(audio_data)
                                except ValueError:
                                    # 如果无法解析为整数，跳过这行数据
                                    print(f"无法解析数据: {line[:50]}...")
            except Exception as e:
                print(f"接收数据错误: {e}")
                self.connected = False
                self.connection_status.emit(False, f"连接错误: {str(e)}")
                break

class SimpleAudioVisualizer(QMainWindow):
    """简化版音频可视化器"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESP32S3 Sense 音频可视化器 (简化版)")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化数据接收器
        self.data_receiver = DataReceiver()
        self.data_receiver.data_received.connect(self.update_audio_data)
        self.data_receiver.connection_status.connect(self.update_connection_status)
        
        # 初始化UI
        self.init_ui()
        
        # 初始化数据
        self.audio_data = []
        self.max_data_points = 1000
        
        # 设置定时器用于更新显示
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)  # 10 FPS
        
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 连接控制区域
        connection_group = QGroupBox("连接设置")
        connection_layout = QGridLayout()
        connection_group.setLayout(connection_layout)
        
        # IP地址设置
        connection_layout.addWidget(QLabel("设备IP:"), 0, 0)
        self.ip_input = QTextEdit()
        self.ip_input.setMaximumHeight(30)
        self.ip_input.setText("192.168.1.100")
        connection_layout.addWidget(self.ip_input, 0, 1)
        
        # 端口设置
        connection_layout.addWidget(QLabel("端口:"), 1, 0)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(8080)
        connection_layout.addWidget(self.port_input, 1, 1)
        
        # 连接按钮
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.toggle_connection)
        connection_layout.addWidget(self.connect_btn, 2, 0, 1, 2)
        
        # 连接状态
        self.connection_status = QLabel("未连接")
        self.connection_status.setStyleSheet("color: red; font-weight: bold;")
        connection_layout.addWidget(self.connection_status, 3, 0, 1, 2)
        
        main_layout.addWidget(connection_group)
        
        # 数据显示区域
        data_group = QGroupBox("音频数据")
        data_layout = QVBoxLayout()
        data_group.setLayout(data_layout)
        
        # 音频波形显示（使用进度条模拟）
        self.audio_display = QTextEdit()
        self.audio_display.setMaximumHeight(200)
        self.audio_display.setReadOnly(True)
        data_layout.addWidget(self.audio_display)
        
        # 数据统计
        self.data_stats = QLabel("等待数据...")
        data_layout.addWidget(self.data_stats)
        
        main_layout.addWidget(data_group)
        
        # 控制区域
        control_group = QGroupBox("控制")
        control_layout = QHBoxLayout()
        control_group.setLayout(control_layout)
        
        # 数据点数量设置
        control_layout.addWidget(QLabel("显示数据点:"))
        self.data_points_input = QSpinBox()
        self.data_points_input.setRange(100, 5000)
        self.data_points_input.setValue(1000)
        self.data_points_input.valueChanged.connect(self.update_max_data_points)
        control_layout.addWidget(self.data_points_input)
        
        # 图表类型选择
        control_layout.addWidget(QLabel("图表类型:"))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["波形图", "频谱图", "瀑布图"])
        self.chart_type_combo.currentTextChanged.connect(self.change_chart_type)
        control_layout.addWidget(self.chart_type_combo)
        
        # 清除数据按钮
        self.clear_btn = QPushButton("清除数据")
        self.clear_btn.clicked.connect(self.clear_data)
        control_layout.addWidget(self.clear_btn)
        
        control_layout.addStretch()
        main_layout.addWidget(control_group)
        
    def toggle_connection(self):
        """切换连接状态"""
        if not self.data_receiver.connected:
            # 尝试连接
            ip = self.ip_input.toPlainText().strip()
            port = self.port_input.value()
            self.data_receiver.host = ip
            self.data_receiver.port = port
            
            if self.data_receiver.connect_to_device():
                self.data_receiver.start_receiving()
                self.connect_btn.setText("断开")
        else:
            # 断开连接
            self.data_receiver.disconnect_from_device()
            self.connect_btn.setText("连接")
            
    def update_connection_status(self, connected, message):
        """更新连接状态显示"""
        if connected:
            self.connection_status.setText(message)
            self.connection_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.connection_status.setText(message)
            self.connection_status.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setText("连接")
            
    def update_audio_data(self, data):
        """更新音频数据"""
        self.audio_data.extend(data)
        
        # 限制数据点数量
        if len(self.audio_data) > self.max_data_points:
            self.audio_data = self.audio_data[-self.max_data_points:]
            
    def update_display(self):
        """更新显示"""
        if self.audio_data:
            current_chart_type = self.chart_type_combo.currentText()
            
            if current_chart_type == "波形图":
                # 显示最新的音频数据
                display_data = self.audio_data[-100:]  # 显示最后100个数据点
                display_text = "音频波形 (时域):\n"
                
                # 创建简单的文本波形
                for i, value in enumerate(display_data):
                    # 将音频值映射到字符，考虑正负值
                    normalized = (value + 32768) / 65536.0  # 映射到0-1
                    bar_length = int(normalized * 50)  # 最大50个字符
                    bar = "█" * bar_length
                    display_text += f"{i:3d}: {bar} ({value:6d})\n"
                
                self.audio_display.setText(display_text)
                
            elif current_chart_type == "频谱图":
                # 简单的频谱显示
                if len(self.audio_data) >= 64:
                    # 计算简单的频谱（使用最近的数据）
                    recent_data = self.audio_data[-512:] if len(self.audio_data) >= 512 else self.audio_data
                    display_text = "音频频谱 (频域):\n"
                    
                    # 简单的频域分析 - 模拟FFT
                    chunk_size = 16  # 增加chunk大小提高频率分辨率
                    num_chunks = len(recent_data) // chunk_size
                    
                    for i in range(num_chunks):
                        start_idx = i * chunk_size
                        end_idx = start_idx + chunk_size
                        chunk = recent_data[start_idx:end_idx]
                        
                        if chunk:
                            # 计算RMS值
                            rms = np.sqrt(np.mean(np.array(chunk) ** 2))
                            
                            # 转换为dB (参考值32768)
                            if rms > 0:
                                db = 20 * np.log10(max(rms, 1e-6) / 32768.0)
                                # 限制dB范围
                                db = max(-60, min(0, db))
                                # 归一化到0-50的范围
                                normalized_db = max(0, min(50, db + 60))  # -60dB到0dB映射到0-50
                                bar_length = int(normalized_db)
                                bar = "█" * bar_length
                                freq = i * 16000 / (2 * num_chunks)  # 估算频率
                                display_text += f"{freq:5.0f}Hz: {bar} ({db:5.1f}dB)\n"
                    
                    self.audio_display.setText(display_text)
                    
            elif current_chart_type == "瀑布图":
                # 简单的瀑布图显示
                display_data = self.audio_data[-50:]  # 显示最后50个数据点
                display_text = "音频瀑布图 (时频):\n"
                
                for i, value in enumerate(display_data):
                    # 计算信号强度
                    intensity = abs(value)
                    normalized = intensity / 32768.0
                    bar_length = int(normalized * 50)
                    bar = "█" * bar_length
                    display_text += f"T{i:2d}: {bar} ({intensity:5d})\n"
                
                self.audio_display.setText(display_text)
            
            # 更新统计信息
            stats_text = f"图表类型: {current_chart_type}\n"
            stats_text += f"数据点数量: {len(self.audio_data)}\n"
            stats_text += f"最大值: {max(self.audio_data) if self.audio_data else 0}\n"
            stats_text += f"最小值: {min(self.audio_data) if self.audio_data else 0}\n"
            stats_text += f"平均值: {sum(self.audio_data)/len(self.audio_data) if self.audio_data else 0:.2f}\n"
            stats_text += f"最新值: {self.audio_data[-1] if self.audio_data else 0}"
            self.data_stats.setText(stats_text)
            
    def update_max_data_points(self):
        """更新最大数据点数量"""
        self.max_data_points = self.data_points_input.value()
        
    def clear_data(self):
        """清除数据"""
        self.audio_data = []
        self.audio_display.setText("数据已清除")
        
    def change_chart_type(self, chart_type):
        """切换图表类型"""
        print(f"切换到图表类型: {chart_type}")
        # 清除显示
        self.audio_display.setText(f"切换到 {chart_type}...")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = SimpleAudioVisualizer()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 