#!/usr/bin/env python3
"""
GUI测试脚本 - 测试图表类型切换功能
"""

import sys
import time
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer

class TestDataGenerator:
    """测试数据生成器"""
    
    def __init__(self):
        self.data = []
        self.frequency = 440
        self.sample_rate = 16000
        self.time = 0
        
    def generate_sine_wave(self, count=1024):
        """生成正弦波数据"""
        data = []
        for i in range(count):
            # 生成正弦波 + 噪声
            sine_wave = 1000 * (time.time() + i / self.sample_rate)
            noise = random.uniform(-100, 100)
            sample = int(sine_wave + noise)
            data.append(sample)
        return data

class TestWindow(QMainWindow):
    """测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 测试按钮
        self.test_btn = QPushButton("测试图表切换")
        self.test_btn.clicked.connect(self.test_chart_switching)
        layout.addWidget(self.test_btn)
        
        # 状态标签
        self.status_label = QLabel("准备测试...")
        layout.addWidget(self.status_label)
        
        # 数据生成器
        self.data_generator = TestDataGenerator()
        
    def test_chart_switching(self):
        """测试图表切换功能"""
        self.status_label.setText("开始测试图表切换...")
        
        # 模拟数据
        test_data = self.data_generator.generate_sine_wave(1024)
        
        # 测试不同的图表类型
        chart_types = ["波形图", "频谱图", "瀑布图"]
        
        for chart_type in chart_types:
            self.status_label.setText(f"测试 {chart_type}...")
            QApplication.processEvents()  # 更新UI
            time.sleep(1)  # 等待1秒
            
        self.status_label.setText("测试完成!")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 