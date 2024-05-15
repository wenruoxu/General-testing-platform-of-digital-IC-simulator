import pandas as pd
import json
import matplotlib.pyplot as plt

file_iv = './results/integrated_results_iv_amount_2024-05-09_20-55-04.json'
file_qs = './results/integrated_results_qs_amount_2024-05-09_20-55-04.json'

# file_iv = './results/integrated_results_iv_BW_2024-05-09_21-48-39.json'
# file_qs = './results/integrated_results_qs_BW_2024-05-09_21-48-39.json'

# file_iv = './results/integrated_results_iv_N_2024-05-09_21-24-44.json'
# file_qs = './results/integrated_results_qs_N_2024-05-09_21-24-44.json'

# 初始化一个空列表来存储DataFrame
df_list = []

# 读取并转换第一个文件
with open(file_iv, 'r') as f:
    data_iv = json.load(f)
    data_iv["simulate_time"] = ["00:" + time for time in data_iv["simulate_time"]]
    print(data_iv['config_infos'])
    df_iv = pd.DataFrame({
        "values": pd.to_numeric(data_iv["values"]),
        "simulate_time": pd.to_timedelta(data_iv["simulate_time"]).total_seconds()
    })
    df_list.append(df_iv)  # 将DataFrame添加到列表中

# 读取并转换第二个文件
with open(file_qs, 'r') as f:
    data_qs = json.load(f)
    print(data_qs['simulate_time'])
    # data_qs["simulate_time"] = ["00:" + time for time in data_qs["simulate_time"]]
    df_qs = pd.DataFrame({
        "values": pd.to_numeric(data_qs["values"]),
        "simulate_time": pd.to_timedelta(data_qs["simulate_time"]).total_seconds()
    })
    df_list.append(df_qs)  # 将DataFrame添加到列表中

# 绘制IV的仿真时间
plt.figure(figsize=(10, 6))  # 设置图表大小
plt.xscale('log')  # 设置x轴为对数坐标import React from
plt.yscale('log')  # 设置y轴为对数坐标
plt.plot(df_iv['values'], df_iv['simulate_time'], label='IV', marker='o', linestyle='-')

# 绘制QS的仿真时间
plt.plot(df_qs['values'], df_qs['simulate_time'], label='QS', marker='x', linestyle='--')

# 添加图表标题和坐标轴标签
plt.title('Simulate Time Comparison')
plt.xlabel('Values')
plt.ylabel('Simulate Time (seconds)')

# 显示图例
plt.legend()


# # 创建config_infos的DataFrame并绘制为表格
# df_config = pd.DataFrame([data_iv['config_infos']])
# plt.subplot(212, frame_on=False)  # 分配下半部分绘制表格
# plt.axis('off')  # 关闭坐标轴
# tbl = plt.table(cellText=df_config.values, colLabels=df_config.columns, cellLoc='center', loc='center',
# bbox=[0, 0, 1, 1])
# tbl.auto_set_font_size(False)
# tbl.set_fontsize(10)
# tbl.scale(1.2, 1.2)  # 调整表格大小


# 显示网格
plt.grid(True)
plt.savefig('simulate_time_comparison.png', dpi=300)  #

# 显示图表
plt.show()
