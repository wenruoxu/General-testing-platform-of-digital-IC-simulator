import glob
import json
import pandas as pd


def list_one(data):
    # 访问并输出subject的值
    subject_value = data["subject"]
    print(subject_value)
    # 将JSON字符串解析为Python字典
    # Convert the JSON data to a DataFrame
    df = pd.DataFrame({
        "values": pd.to_numeric(data["values"]),
        "compile_time": data["compile_time"],
        "compile_memory": pd.to_numeric(data["compile_memory"]),
        "simulate_time": data["simulate_time"],
        "simulate_memory": pd.to_numeric(data["simulate_memory"])
    })
    # Display the DataFrame
    print(df)


def list_all():
    # 遍历当前文件夹中所有以'integrated'开头的json文件
    for file_name in glob.glob('./integrated*.json'):
        with open(file_name, 'r') as file:
            datas = json.load(file)
            print(file_name)
            list_one(datas)


useful = ['./integrated_results_*_BW_2024-05-09_21-48-39.json',
          './integrated_results_*_BW_2024-05-09_21-43-42.json',
          './integrated_results_*_N_2024-05-09_21-24-44.json',
          './integrated_results_*_N_2024-05-09_21-06-42.json',
          './integrated_results_*_amount_2024-05-09_20-55-04.json']

for one_useful in useful:
    for file_name in glob.glob(one_useful):
        with open(file_name, 'r') as file:
            datas = json.load(file)
            print(file_name)
            list_one(datas)
        with open('./results/'+file_name, 'w') as file:
            json.dump(datas, file, indent=4)


"""
useful:
qs性能不好但是还没有爆内存
./integrated_results_*_BW_2024-05-09_21-48-39.json
qs直接爆内存了
./integrated_results_*_BW_2024-05-09_21-43-42.json

特殊（极端）场景在qs的优势
./integrated_results_*_N_2024-05-09_21-06-42.json

./integrated_results_*_N_2024-05-09_21-24-44.json
./integrated_results_*_amount_2024-05-09_20-55-04.json

"""
