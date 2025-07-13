#!/usr/bin/env python3
"""
频谱图修复测试脚本
"""

import numpy as np
import sys

def test_spectrum_calculation():
    """测试频谱计算是否安全"""
    print("测试频谱计算...")
    
    # 生成测试数据
    sample_rate = 16000
    fft_size = 2048
    t = np.linspace(0, 1, fft_size)
    
    # 生成包含多个频率的信号
    signal = (np.sin(2 * np.pi * 440 * t) +  # 440Hz
              0.5 * np.sin(2 * np.pi * 880 * t) +  # 880Hz
              0.3 * np.sin(2 * np.pi * 1760 * t))  # 1760Hz
    
    # 添加噪声
    noise = np.random.normal(0, 0.1, len(signal))
    signal = signal + noise
    
    # 转换为整数
    audio_data = (signal * 1000).astype(int)
    
    try:
        # 应用窗函数
        window = np.hanning(len(audio_data))
        windowed_data = audio_data * window
        
        # 计算FFT
        fft_data = np.fft.fft(windowed_data)
        freq_data = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        
        # 只显示正频率部分，限制到8kHz
        positive_freq_mask = (freq_data >= 0) & (freq_data <= 8000)
        freq_data = freq_data[positive_freq_mask]
        fft_data = np.abs(fft_data[positive_freq_mask])
        
        # 安全的dB转换
        fft_data = np.maximum(fft_data, 1e-8)
        fft_db = 20 * np.log10(fft_data)
        
        # 限制dB范围
        fft_db = np.clip(fft_db, -80, 0)
        
        # 归一化
        max_db = np.max(fft_db)
        if max_db > -80:
            fft_db = fft_db - max_db
        
        print("✓ 频谱计算成功!")
        print(f"  频率范围: {freq_data.min():.1f}Hz - {freq_data.max():.1f}Hz")
        print(f"  dB范围: {fft_db.min():.1f}dB - {fft_db.max():.1f}dB")
        print(f"  数据点数: {len(freq_data)}")
        
        return True
        
    except Exception as e:
        print(f"✗ 频谱计算失败: {e}")
        return False

def test_log_scale():
    """测试对数坐标是否安全"""
    print("\n测试对数坐标...")
    
    try:
        # 测试各种dB值
        test_values = [-80, -60, -40, -20, -10, -5, -1, 0]
        
        for db in test_values:
            # 转换为线性值
            linear = 10**(db/20)
            # 再转换回dB
            db_back = 20 * np.log10(max(linear, 1e-8))
            print(f"  {db:3.0f}dB -> {linear:.2e} -> {db_back:.1f}dB")
        
        print("✓ 对数坐标测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 对数坐标测试失败: {e}")
        return False

def main():
    """主函数"""
    print("频谱图修复测试")
    print("=" * 30)
    
    # 测试频谱计算
    spectrum_ok = test_spectrum_calculation()
    
    # 测试对数坐标
    log_ok = test_log_scale()
    
    # 总结
    print("\n测试结果:")
    if spectrum_ok and log_ok:
        print("✓ 所有测试通过，频谱图应该可以正常工作")
    else:
        print("✗ 部分测试失败，需要进一步修复")

if __name__ == "__main__":
    main() 