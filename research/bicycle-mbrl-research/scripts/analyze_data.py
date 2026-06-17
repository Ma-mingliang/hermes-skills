#!/usr/bin/env python3
"""
自行车数据分析脚本
用于分析微信小程序导出的CSV数据

用法：
    python analyze_data.py bike_data.csv
    python analyze_data.py bike_data.csv -o my_analysis
    python analyze_data.py bike_data.csv --no-plot
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import argparse
import os

def load_data(csv_file):
    """加载CSV数据"""
    try:
        df = pd.read_csv(csv_file)
        print(f"成功加载数据: {len(df)} 条记录")
        print(f"时间范围: {df['timestamp'].iloc[0]} - {df['timestamp'].iloc[-1]}")
        print(f"模式分布:")
        print(df['modeId'].value_counts().sort_index())
        return df
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None

def plot_response(df, output_dir=None):
    """绘制响应曲线"""
    df['time_ms'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1000.0
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    axes[0].plot(df['time_ms'], df['pitch'], 'b-', linewidth=1)
    axes[0].set_xlabel('时间 (秒)')
    axes[0].set_ylabel('俯仰角 (度)')
    axes[0].set_title('俯仰角响应曲线')
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    axes[1].plot(df['time_ms'], df['roll'], 'g-', linewidth=1)
    axes[1].set_xlabel('时间 (秒)')
    axes[1].set_ylabel('横滚角 (度)')
    axes[1].set_title('横滚角响应曲线')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    axes[2].plot(df['time_ms'], df['batt'], 'r-', linewidth=1)
    axes[2].set_xlabel('时间 (秒)')
    axes[2].set_ylabel('电池电压 (V)')
    axes[2].set_title('电池电压变化')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_file = os.path.join(output_dir, f'response_plot_{timestamp}.png')
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"图形已保存: {plot_file}")
    
    plt.show()

def analyze_performance(df):
    """分析性能指标"""
    print("\n" + "="*60)
    print("性能分析")
    print("="*60)
    
    df['time_ms'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1000.0
    pitch = df['pitch']
    
    print(f"\n俯仰角统计:")
    print(f"  均值: {pitch.mean():.4f} 度")
    print(f"  标准差: {pitch.std():.4f} 度")
    print(f"  最小值: {pitch.min():.4f} 度")
    print(f"  最大值: {pitch.max():.4f} 度")
    print(f"  峰峰值: {pitch.max() - pitch.min():.4f} 度")
    
    steady_state_start = int(len(df) * 0.9)
    steady_state_pitch = pitch.iloc[steady_state_start:]
    steady_state_error = steady_state_pitch.mean()
    
    print(f"\n稳态分析（最后10%数据）:")
    print(f"  稳态均值: {steady_state_error:.4f} 度")
    print(f"  稳态标准差: {steady_state_pitch.std():.4f} 度")
    
    return {
        'mean': pitch.mean(),
        'std': pitch.std(),
        'steady_state_error': steady_state_error,
    }

def analyze_by_mode(df):
    """按模式分析数据"""
    print("\n" + "="*60)
    print("按模式分析")
    print("="*60)
    
    for mode_id in sorted(df['modeId'].unique()):
        mode_data = df[df['modeId'] == mode_id]
        mode_name = {0: 'Idle', 1: 'Segway', 2: 'Bike'}.get(mode_id, f'Unknown({mode_id})')
        
        print(f"\n模式 {mode_name} ({mode_id}):")
        print(f"  数据点数: {len(mode_data)}")
        print(f"  俯仰角均值: {mode_data['pitch'].mean():.4f} 度")
        print(f"  俯仰角标准差: {mode_data['pitch'].std():.4f} 度")

def main():
    parser = argparse.ArgumentParser(description='自行车数据分析工具')
    parser.add_argument('csv_file', help='CSV数据文件路径')
    parser.add_argument('--output-dir', '-o', help='输出目录', default='analysis_output')
    parser.add_argument('--no-plot', action='store_true', help='不显示图形')
    
    args = parser.parse_args()
    
    df = load_data(args.csv_file)
    if df is None:
        return
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    if not args.no_plot:
        plot_response(df, args.output_dir)
    
    analyze_performance(df)
    analyze_by_mode(df)

if __name__ == '__main__':
    main()
