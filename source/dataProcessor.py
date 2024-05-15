import glob
import json
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import OrderedDict

"""
ToDo:
    if you want to test BW, remember generate new initial file.
"""


class DataProcessor:
    def __init__(self, logger, infos, **kwargs):
        self.qs_df = None
        self.iv_df = None
        self.result = None
        self.logger = logger
        self.infos = infos

        self.description = None
        self.saveOriginal = None
        self.format = None

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.logger.info(f"\nconfiguration of DataProcessor class:{kwargs}")

    def process(self, subject):
        self.integrate_results(subject)
        self.json2df(subject)
        self.load_data()

        # ToDo Test
        self.add_infos()
        self.clear_results()
        self.copy_files_to_useful()
        pass

    def add_infos(self):
        json_files = glob.glob('../outputs/result/integrated*.json')

        for json_file_path in json_files:
            # 读取原始JSON文件
            with open(json_file_path, 'r') as file:
                # 加载JSON内容为字典
                original_data = json.load(file, object_pairs_hook=OrderedDict)

                # 将新字典作为第一项插入
            # 创建一个新的OrderedDict，将self.infos作为一个整体（单独的结构体）插入到开始位置
            updated_data = OrderedDict()
            updated_data['config_infos'] = self.infos  # 将self.infos作为一个整体添加
            for key, value in original_data.items():
                updated_data[key] = value

            # 将更新后的字典写回JSON文件
            with open(json_file_path, 'w') as file:
                json.dump(updated_data, file, indent=4)
            self.logger.info(f"Updated file: {json_file_path} with new data.")
            self.logger.info(f"Updated data: \n{updated_data}")

    def load_data(self):
        if check_final_exist('iv'):
            self.iv_df = pd.read_csv('../outputs/result/final_result_iv.csv')
            self.logger.info(f'\nThe dataframe of IVerilog is following:\n{self.iv_df}')
        else:
            self.logger.warning("FINAL RESULT: No files with 'iv' in their names.")
        if check_final_exist('qs'):
            self.qs_df = pd.read_csv('../outputs/result/final_result_qs.csv')
            self.logger.info(f'\nThe dataframe of Questasim is following: \n{self.qs_df}')
        else:
            self.logger.warning("FINAL RESULT: No files with 'qs' in their names.")
        pass

    def integrate_results(self, subject):
        if check_original_exist(subject, 'iv'):
            self.logger.info("Found files with 'iv' in their names.")
            integrate_results('iv', subject)
            self.logger.info(f"Integrated results of 'IVerilog' at: ../outputs/result/result_iv_{subject}.json")
        if check_original_exist(subject, 'qs'):
            self.logger.info("Found files with 'qs' in their names.")
            integrate_results('qs', subject)
            self.logger.info(f"Integrated results of 'Questasim' at: ../outputs/result/result_qs_{subject}.json")

    def clear_results(self):
        # 查找所有以result为开头的文件
        result_files = glob.glob('../outputs/result/result*.json')
        # 遍历并删除这些文件
        for file_path in result_files:
            try:
                os.remove(file_path)
                self.logger.info(f"Deleted file: {file_path}")
            except Exception as e:
                self.logger.error(f"Error deleting file {file_path}: {e}")

    def json2df(self, subject):

        if check_integrated_exist(subject, 'iv'):
            simulator = 'iv'
            generate_final_result(simulator, subject)
            self.logger.info(f"Final results of 'IVerilog' at:" + f'../outputs/result/final_result_{simulator}.csv')
        if check_integrated_exist(subject, 'qs'):
            simulator = 'qs'
            generate_final_result(simulator, subject)
            self.logger.info(f"Final results of 'Questasim' at:" + f'../outputs/result/final_result_{simulator}.csv')

    def copy_files_to_useful(self):
        source_dir = '../outputs/result/'
        target_dir = '../outputs/result/useful/'

        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)

        # 获取源目录中的所有文件路径
        files = glob.glob(source_dir + '*')
        for file_path in files:
            # 构建目标文件的路径
            target_file_path = os.path.join(target_dir, os.path.basename(file_path))
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # 分割文件名和扩展名
            file_name, file_extension = os.path.splitext(target_file_path)
            # 在文件名和扩展名之间插入当前时间
            target_file_path = f"{file_name}_{current_time}{file_extension}"

            # 复制文件
            try:
                shutil.copy(file_path, target_file_path)
                self.logger.info(f"Copied file: {file_path} to {target_file_path}")
            except Exception as e:
                self.logger.info(f"Error copying file {file_path} to {target_file_path}: {e}")


def integrate_results(simulator, subject):
    integrated_results = {
        "simulator": "",
        "subject": subject,
        "values": [],
        "compile_time": [],
        "compile_memory": [],
        "simulate_time": [],
        "simulate_memory": []
    }

    json_files = glob.glob(f'../outputs/result/result_{simulator}_{subject}_*.json')
    # 按照文件的修改时间排序
    json_files.sort(key=os.path.getmtime)

    # 遍历排序后的文件列表
    for file_path in json_files:
        # 读取并处理每个文件
        with open(file_path, 'r') as file:
            data = json.load(file)
            # 更新integrated_results字典
            integrated_results["simulator"] = data["info"]["simulator"]
            integrated_results["values"].append(data["info"]["value"])
            integrated_results["compile_time"].append(data["compile_time"])
            integrated_results["compile_memory"].append(data["compile_memory"])
            integrated_results["simulate_time"].append(data["simulate_time"])
            integrated_results["simulate_memory"].append(data["simulate_memory"])

    # 写入整合后的结果到一个新的JSON文件
    output_file_path = f'../outputs/result/integrated_results_{simulator}_{subject}.json'
    with open(output_file_path, 'w') as file:
        json.dump(integrated_results, file, indent=4)


def check_original_exist(subject, simulator):
    # 检查是否存在包含特定字符的文件
    json_files = glob.glob(f'../outputs/result/result_{simulator}_{subject}_*.json')
    return len(json_files) > 0


def check_integrated_exist(subject, simulator):
    # 检查是否存在包含特定字符的文件
    json_files = glob.glob(f'../outputs/result/integrated_results_{simulator}*.json')
    return len(json_files) > 0


def check_final_exist(simulator):
    # 检查是否存在包含特定字符的文件
    json_files = glob.glob(f'../outputs/result/final_result_{simulator}.csv')
    return len(json_files) > 0


def generate_final_result(simulator, subject):
    # 读取JSON文件
    file_path = f'../outputs/result/integrated_results_{simulator}_{subject}.json'  # 请替换为实际的文件路径
    with open(file_path, 'r') as file:
        data = json.load(file)
    data["compile_time"] = ["00:" + time for time in data["compile_time"]]
    if simulator == 'iv':
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
    df.to_csv(f'../outputs/result/final_result_{simulator}.csv', index=False)


def generate_graph(df):
    # 假设df是你的DataFrame
    # 绘制value与compile_time的关系图
    plt.figure(figsize=(10, 6))  # 设置图表大小
    plt.plot(df['values'], df['compile_time'], marker='o', linestyle='-', color='b')  # 绘制线图
    plt.title('Compile Time vs Values')  # 设置图表标题
    plt.xlabel('Values')  # 设置x轴标签
    plt.ylabel('Compile Time (seconds)')  # 设置y轴标签
    plt.grid(True)  # 显示网格
    plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域

    # 保存图表到result/useful文件夹中
    plt.savefig('../outputs/result/useful/compile_time_vs_values.png')
    plt.close()  # 关闭图表，释放内存
    pass
