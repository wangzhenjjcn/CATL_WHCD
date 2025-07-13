#!/usr/bin/env python3
"""
安全的频谱图实现 - 避免溢出问题
"""

import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import sys

class SafeSpectrumAnalyzer:
    """安全的频谱分析器"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.fft_size = 2048
        self.freq_resolution = self.sample_rate / self.fft_size
        
    def safe_fft(self, audio_data):
        """安全的FFT计算"""
        if len(audio_data) < self.fft_size:
            # 如果数据不足，用零填充
            padded_data = np.zeros(self.fft_size)
            padded_data[:len(audio_data)] = audio_data
            audio_data = padded_data
        else:
            # 取最近的FFT_SIZE个样本
            audio_data = audio_data[-self.fft_size:]
        
        # 应用窗函数
        window = np.hanning(self.fft_size)
        windowed_data = audio_data * window
        
        # 计算FFT
        fft_result = np.fft.fft(windowed_data)
        
        # 计算幅度谱
        magnitude = np.abs(fft_result)
        
        # 计算频率轴
        freq_axis = np.fft.fftfreq(self.fft_size, 1/self.sample_rate)
        
        # 只取正频率部分
        positive_mask = freq_axis >= 0
        freq_axis = freq_axis[positive_mask]
        magnitude = magnitude[positive_mask]
        
        return freq_axis, magnitude
    
    def safe_db_conversion(self, magnitude):
        """安全的dB转换"""
        # 设置最小阈值避免log(0)
        min_magnitude = 1e-8
        magnitude = np.maximum(magnitude, min_magnitude)
        
        # 转换为dB
        db = 20 * np.log10(magnitude)
        
        # 限制dB范围
        db = np.clip(db, -80, 0)
        
        return db
    
    def normalize_spectrum(self, db_spectrum):
        """归一化频谱"""
        max_db = np.max(db_spectrum)
        if max_db > -80:
            normalized_db = db_spectrum - max_db
        else:
            normalized_db = db_spectrum
        
        return normalized_db

class SafeSpectrumWindow(QMainWindow):
    """安全的频谱显示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("安全频谱分析器")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建图表
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLogMode(x=False, y=True)
        self.plot_widget.setLabel('left', '幅度 (dB)')
        self.plot_widget.setLabel('bottom', '频率 (Hz)')
        self.plot_widget.setTitle('安全频谱分析')
        self.plot_widget.setXRange(0, 8000)  # 限制到8kHz避免溢出
        self.plot_widget.setYRange(-60, 0)
        
        layout.addWidget(self.plot_widget)
        
        # 创建频谱分析器
        self.analyzer = SafeSpectrumAnalyzer()
        
        # 模拟数据
        self.audio_data = []
        
        # 定时器更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_spectrum)
        self.timer.start(100)  # 10 FPS
        
    def generate_test_data(self):
        """生成测试数据"""
        # 生成包含多个频率的测试信号
        t = np.linspace(0, 1, 2048)
        signal = (np.sin(2 * np.pi * 440 * t) +  # 440Hz
                 0.5 * np.sin(2 * np.pi * 880 * t) +  # 880Hz
                 0.3 * np.sin(2 * np.pi * 1760 * t))  # 1760Hz
        
        # 添加噪声
        noise = np.random.normal(0, 0.1, len(signal))
        signal = signal + noise
        
        return (signal * 1000).astype(int)
    
    def update_spectrum(self):
        """更新频谱显示"""
        # 生成测试数据
        test_data = self.generate_test_data()
        
        try:
            # 计算频谱
            freq_axis, magnitude = self.analyzer.safe_fft(test_data)
            
            # 转换为dB
            db_spectrum = self.analyzer.safe_db_conversion(magnitude)
            
            # 归一化
            normalized_db = self.analyzer.normalize_spectrum(db_spectrum)
            
            # 限制频率范围
            freq_mask = freq_axis <= 8000  # 限制到8kHz
            freq_axis = freq_axis[freq_mask]
            normalized_db = normalized_db[freq_mask]
            
            # 更新图表
            self.plot_widget.clear()
            self.plot_widget.plot(freq_axis, normalized_db, pen=pg.mkPen('r', width=2))
            
        except Exception as e:
            print(f"频谱更新错误: {e}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = SafeSpectrumWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 