import sys
import json
import socket
import threading
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QTextEdit, QGroupBox,
                             QGridLayout, QSpinBox, QComboBox)
from PyQt6.QtCore import QTimer, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont, QPalette, QColor
import pyqtgraph as pg
import numpy as np

class DataReceiver(QObject):
    """数据接收器类，用于从ESP32S3接收数据"""
    data_received = pyqtSignal(list)
    connection_status = pyqtSignal(bool, str)
    
    def __init__(self, host='192.168.0.194', port=8080):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        self.buffer = ""
        
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
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
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
                    self.buffer += data.decode('utf-8')
                    
                    while '\n' in self.buffer:
                        line, self.buffer = self.buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            try:
                                json_data = json.loads(line)
                                if 'audio_data' in json_data:
                                    audio_data = json_data['audio_data']
                                    self.data_received.emit(audio_data)
                            except json.JSONDecodeError:
                                try:
                                    audio_data = [int(x) for x in line.split(',') if x.strip()]
                                    if audio_data:
                                        self.data_received.emit(audio_data)
                                except ValueError:
                                    print(f"无法解析数据: {line[:50]}...")
            except Exception as e:
                print(f"接收数据错误: {e}")
                self.connected = False
                self.connection_status.emit(False, f"连接错误: {str(e)}")
                break

class WorkingAudioVisualizer(QMainWindow):
    """工作版音频可视化器 - 避免所有坐标问题"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESP32S3 Sense 音频可视化器 (工作版)")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化数据接收器
        self.data_receiver = DataReceiver()
        self.data_receiver.data_received.connect(self.update_audio_data)
        self.data_receiver.connection_status.connect(self.update_connection_status)
        
        # 初始化UI
        self.init_ui()
        
        # 初始化数据
        self.audio_data = []
        self.max_data_points = 1000
        
        # 设置定时器用于更新图表
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plots)
        self.update_timer.start(50)  # 20 FPS
        
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 左侧控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel, 1)
        
        # 右侧图表区域
        chart_panel = self.create_chart_panel()
        main_layout.addWidget(chart_panel, 4)
        
    def create_control_panel(self):
        """创建控制面板"""
        control_widget = QWidget()
        control_layout = QVBoxLayout()
        control_widget.setLayout(control_layout)
        
        # 连接设置组
        connection_group = QGroupBox("连接设置")
        connection_layout = QGridLayout()
        connection_group.setLayout(connection_layout)
        
        # IP地址设置
        connection_layout.addWidget(QLabel("设备IP:"), 0, 0)
        self.ip_input = QTextEdit()
        self.ip_input.setMaximumHeight(30)
        self.ip_input.setText("192.168.0.194")
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
        
        control_layout.addWidget(connection_group)
        
        # 显示设置组
        display_group = QGroupBox("显示设置")
        display_layout = QVBoxLayout()
        display_group.setLayout(display_layout)
        
        # 数据点数量设置
        display_layout.addWidget(QLabel("显示数据点:"))
        self.data_points_input = QSpinBox()
        self.data_points_input.setRange(100, 5000)
        self.data_points_input.setValue(1000)
        self.data_points_input.valueChanged.connect(self.update_max_data_points)
        display_layout.addWidget(self.data_points_input)
        
        # 图表类型选择
        display_layout.addWidget(QLabel("图表类型:"))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["波形图", "频谱图", "瀑布图"])
        self.chart_type_combo.currentTextChanged.connect(self.change_chart_type)
        display_layout.addWidget(self.chart_type_combo)
        
        control_layout.addWidget(display_group)
        
        # 数据信息组
        info_group = QGroupBox("数据信息")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)
        
        self.data_info = QTextEdit()
        self.data_info.setMaximumHeight(100)
        self.data_info.setReadOnly(True)
        info_layout.addWidget(self.data_info)
        
        control_layout.addWidget(info_group)
        
        control_layout.addStretch()
        return control_widget
        
    def create_chart_panel(self):
        """创建图表面板"""
        chart_widget = QWidget()
        chart_layout = QVBoxLayout()
        chart_widget.setLayout(chart_layout)
        
        # 创建PyQtGraph窗口
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setLabel('left', '振幅')
        self.graph_widget.setLabel('bottom', '时间')
        self.graph_widget.setTitle('ESP32S3 Sense 音频数据')
        
        # 创建数据曲线
        self.audio_curve = self.graph_widget.plot(pen=pg.mkPen('b', width=2))
        
        chart_layout.addWidget(self.graph_widget)
        return chart_widget
        
    def toggle_connection(self):
        """切换连接状态"""
        if not self.data_receiver.connected:
            ip = self.ip_input.toPlainText().strip()
            port = self.port_input.value()
            self.data_receiver.host = ip
            self.data_receiver.port = port
            
            if self.data_receiver.connect_to_device():
                self.data_receiver.start_receiving()
                self.connect_btn.setText("断开")
        else:
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
        
        if len(self.audio_data) > self.max_data_points:
            self.audio_data = self.audio_data[-self.max_data_points:]
            
    def update_plots(self):
        """更新图表显示"""
        if self.audio_data and hasattr(self, 'audio_curve'):
            current_chart_type = self.chart_type_combo.currentText()
            
            if current_chart_type == "波形图":
                # 波形图 - 显示时域数据
                x_data = np.arange(len(self.audio_data))
                if len(self.audio_data) > 1000:
                    step = len(self.audio_data) // 1000
                    x_data = x_data[::step]
                    y_data = self.audio_data[::step]
                else:
                    y_data = self.audio_data
                self.audio_curve.setData(x_data, y_data)
                
            elif current_chart_type == "频谱图":
                # 频谱图 - 使用线性幅度
                if len(self.audio_data) >= 64:
                    try:
                        recent_data = self.audio_data[-2048:] if len(self.audio_data) >= 2048 else self.audio_data
                        
                        # 应用窗函数
                        window = np.hanning(len(recent_data))
                        windowed_data = recent_data * window
                        
                        # 计算FFT
                        fft_data = np.fft.fft(windowed_data)
                        freq_data = np.fft.fftfreq(len(recent_data), 1/16000)
                        
                        # 只显示正频率部分
                        positive_freq_mask = (freq_data >= 0) & (freq_data <= 8000)
                        freq_data = freq_data[positive_freq_mask]
                        fft_data = np.abs(fft_data[positive_freq_mask])
                        
                        # 归一化到0-1范围
                        if np.max(fft_data) > 0:
                            fft_normalized = fft_data / np.max(fft_data)
                        else:
                            fft_normalized = fft_data
                        
                        self.audio_curve.setData(freq_data, fft_normalized)
                        
                    except Exception as e:
                        print(f"频谱计算错误: {e}")
                        self.audio_curve.setData([], [])
                    
            elif current_chart_type == "瀑布图":
                # 瀑布图 - 显示信号强度
                x_data = np.arange(len(self.audio_data))
                intensity = np.abs(self.audio_data)
                self.audio_curve.setData(x_data, intensity)
            
            # 更新数据信息
            info_text = f"图表类型: {current_chart_type}\n"
            info_text += f"数据点数量: {len(self.audio_data)}\n"
            info_text += f"最大值: {max(self.audio_data) if self.audio_data else 0}\n"
            info_text += f"最小值: {min(self.audio_data) if self.audio_data else 0}\n"
            info_text += f"平均值: {sum(self.audio_data)/len(self.audio_data) if self.audio_data else 0:.2f}"
            self.data_info.setText(info_text)
            
    def update_max_data_points(self):
        """更新最大数据点数量"""
        self.max_data_points = self.data_points_input.value()
        
    def change_chart_type(self, chart_type):
        """切换图表类型"""
        print(f"切换到图表类型: {chart_type}")
        
        # 清除现有图表
        self.graph_widget.clear()
        
        if chart_type == "波形图":
            # 波形图
            self.audio_curve = self.graph_widget.plot(pen=pg.mkPen('b', width=2))
            self.graph_widget.setLogMode(x=False, y=False)
            self.graph_widget.setLabel('left', '振幅')
            self.graph_widget.setLabel('bottom', '时间')
            self.graph_widget.setTitle('ESP32S3 Sense 音频波形')
            self.graph_widget.setYRange(-32768, 32768)
            
        elif chart_type == "频谱图":
            # 频谱图 - 使用线性坐标
            self.audio_curve = self.graph_widget.plot(pen=pg.mkPen('r', width=2))
            self.graph_widget.setLogMode(x=False, y=False)  # 完全避免对数坐标
            self.graph_widget.setLabel('left', '幅度')
            self.graph_widget.setLabel('bottom', '频率 (Hz)')
            self.graph_widget.setTitle('ESP32S3 Sense 音频频谱')
            self.graph_widget.setXRange(0, 8000)
            self.graph_widget.setYRange(0, 1)  # 归一化范围
            
        elif chart_type == "瀑布图":
            # 瀑布图
            self.audio_curve = self.graph_widget.plot(pen=pg.mkPen('g', width=2))
            self.graph_widget.setLogMode(x=False, y=False)
            self.graph_widget.setLabel('left', '强度')
            self.graph_widget.setLabel('bottom', '时间')
            self.graph_widget.setTitle('ESP32S3 Sense 音频瀑布图')
            self.graph_widget.setYRange(0, 32768)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = WorkingAudioVisualizer()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 