import csv
import math
import os

def calculate_SNR(filename):
    # 读取csv文件并提取数值
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        
        # 跳过文件头和列标题行
        for _ in range(10):  # 假设前10行是文件头和标题
            next(reader)
        
        data = [float(row[1]) for row in reader if len(row) > 1]

    # 计算信号平均值
    mean_signal = sum(data) / len(data)

    # 计算信号功率
    signal_power = sum([(s - mean_signal) ** 2 for s in data])

    # 计算噪声功率（使用标准差）
    noise_power = sum([(s - mean_signal) ** 2 for s in data]) / len(data)

    # 计算SNR
    SNR = 10 * math.log10(signal_power / noise_power)
    
    return SNR

folder_path = "csv saver/84_2/"

# 列出84_1文件夹下所有的CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

print(folder_path)
for filename in csv_files:
    full_path = os.path.join(folder_path, filename)
    SNR_value = calculate_SNR(full_path)
    print(f"SNR for {filename}: {SNR_value:.2f} dB")
