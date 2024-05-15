import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import glob


def read_and_plot_results(directory):
    # 读取目录下的所有json文件
    files = glob.glob(os.path.join(directory, '*.json'))

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            config_infos = data['config_infos']
            mode = config_infos.get('mode', 'normal')  # 默认为'normal'模式

            # print(file)

            # 将config_infos转换为DataFrame
            df_config = pd.DataFrame([config_infos])

            # 保存config_infos表格为图片
            fig, ax = plt.subplots(figsize=(8, 2))  # 设置图片大小
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=df_config.values, colLabels=df_config.columns, loc='center')
            plt.savefig(file.replace('.json', '_config_infos.png'), dpi=300, bbox_inches='tight')
            plt.close(fig)

            data["compile_time"] = ["00:" + time for time in data["compile_time"]]
            if 'iv' in file:
                data["simulate_time"] = ["00:" + time for time in data["simulate_time"]]

            df = pd.DataFrame({
                "values": pd.to_numeric(data["values"]),
                "compile_time": pd.to_timedelta(data["compile_time"]).total_seconds(),
                "compile_memory": pd.to_numeric(data["compile_memory"]),
                "simulate_time": pd.to_timedelta(data["simulate_time"]).total_seconds(),
                "simulate_memory": pd.to_numeric(data["simulate_memory"])
            })
            df.sort_values(by=["values"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            pd.set_option('display.max_rows', None)  # 设置Pandas显示选项，以显示所有行

            # 绘制图表# Assuming 'values', 'compile_time', 'compile_memory', 'simulate_time', 'simulate_memory' are column names in the DataFrame 'df'
            values = df['values']
            compile_time = df['compile_time']  # Removed incorrect parenthesis and method call
            compile_memory = df['compile_memory']  # This line is correct if 'compile_memory' is a column in 'df'
            simulate_time = df['simulate_time']  # Removed incorrect method call
            simulate_memory = df['simulate_memory']  # This line is correct if 'simulate_memory' is a column in 'df'

            # 绘制四个图表
            plot_graph(values, compile_time, 'Compile Time (seconds)', file.replace('.json', '_compile_time.png'), mode)
            plot_graph(values, compile_memory, 'Compile Memory (KB)', file.replace('.json', '_compile_memory.png'),
                       mode)
            plot_graph(values, simulate_time, 'Simulate Time (seconds)', file.replace('.json', '_simulate_time.png'),
                       mode)
            plot_graph(values, simulate_memory, 'Simulate Memory (KB)', file.replace('.json', '_simulate_memory.png'),
                       mode)


def plot_graph(x, y, ylabel, filename, mode='normal'):
    plt.figure(figsize=(10, 6))
    if mode == 'log':
        plt.xscale('log')  # 设置x轴为对数坐标import React from
        plt.yscale('log')  # 设置y轴为对数坐标
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title(f'{ylabel} vs Values')
    plt.xlabel('Values')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# 调用函数，假设结果文件存放在当前目录的./result文件夹中
read_and_plot_results('./results')
