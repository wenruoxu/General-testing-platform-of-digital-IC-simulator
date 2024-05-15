import json
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress

data_json1 = """{
    "config_infos": {
        "prototype": "adder",
        "BW": 32,
        "N": 1000000,
        "amount": -1,
        "start": 16,
        "end": 4096,
        "step": 2,
        "mode": "log"
    },
    "simulator": "iv",
    "subject": "amount",
    "values": [
        "16",
        "32",
        "64",
        "128",
        "256",
        "512",
        "1024",
        "2048",
        "4096"
    ],
    "compile_time": [
        "0:00.01",
        "0:00.01",
        "0:00.02",
        "0:00.02",
        "0:00.03",
        "0:00.05",
        "0:00.10",
        "0:00.34",
        "0:01.83"
    ],
    "compile_memory": [
        "34364",
        "34612",
        "34872",
        "35648",
        "36948",
        "39800",
        "45516",
        "56844",
        "79760"
    ],
    "simulate_time": [
        "0:00.33",
        "0:00.59",
        "0:01.08",
        "0:02.08",
        "0:04.01",
        "0:08.27",
        "0:18.01",
        "0:37.69",
        "1:20.52"
    ],
    "simulate_memory": [
        "4476",
        "4576",
        "4792",
        "5252",
        "6196",
        "8060",
        "11668",
        "18960",
        "34004"
    ]
}"""

data_json2 = """{
    "config_infos": {
        "prototype": "adder",
        "BW": 32,
        "N": -1,
        "amount": 4096,
        "start": 10000,
        "end": 10000000,
        "step": 2,
        "mode": "log"
    },
    "simulator": "iv",
    "subject": "N",
    "values": [
        "10000",
        "20000",
        "40000",
        "80000",
        "160000",
        "320000",
        "640000",
        "1280000",
        "2560000",
        "5120000"
    ],
    "compile_time": [
        "0:01.29",
        "0:01.39",
        "0:01.34",
        "0:01.39",
        "0:01.42",
        "0:01.41",
        "0:01.55",
        "0:01.60",
        "0:01.73",
        "0:01.99"
    ],
    "compile_memory": [
        "61540",
        "61540",
        "61540",
        "61540",
        "61540",
        "61540",
        "68392",
        "88512",
        "128396",
        "208532"
    ],
    "simulate_time": [
        "0:00.96",
        "0:01.73",
        "0:03.32",
        "0:06.32",
        "0:12.57",
        "0:24.63",
        "0:50.29",
        "1:41.85",
        "3:25.90",
        "6:56.21"
    ],
    "simulate_memory": [
        "34020",
        "34012",
        "34012",
        "34012",
        "34036",
        "34040",
        "34040",
        "34036",
        "34028",
        "34036"
    ]
}
"""


def static(data_input):
    # global summary_df
    # data = json.loads(data_json)
    print(f"{data_input['simulator']} : {data_input['subject']}")
    data_input["simulate_time"] = ["00:" + time for time in data_input["simulate_time"]]
    df = pd.DataFrame({
        "values": pd.to_numeric(data_input["values"]),
        # "compile_time": pd.to_timedelta(data["compile_time"]).total_seconds(),
        "compile_memory": pd.to_numeric(data_input["compile_memory"]),
        "simulate_time": pd.to_timedelta(data_input["simulate_time"]).total_seconds(),
        "simulate_memory": pd.to_numeric(data_input["simulate_memory"])
    })
    # 计算斜率
    slope, intercept, r_value, p_value, std_err = linregress(df['values'], df['simulate_time'])
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R-squared: {r_value ** 2}")
    # 创建一个包含所需信息的字典
    # 创建一个包含所需信息的字典
    data_summary = {
        "Simulator": [data_input['simulator']],
        "Subject": [data_input['subject']],
        "Slope": [f"{slope:.5e}"],
        "Intercept": [f"{intercept:.5e}"],
        "R-squared": [f"{r_value ** 2:.5e}"],
        "P-value": [f"{p_value:.5e}"],
        "Std Err": [f"{std_err:.5e}"]
    }
    # 将字典转换为DataFrame
    summary_df = pd.DataFrame(data_summary)

    # 绘制DataFrame作为表格的图像
    # 绘制DataFrame作为表格的图像
    fig, ax = plt.subplots(figsize=(10, 4))  # 增加图像大小以提供更多空间
    ax.axis('off')  # 关闭坐标轴
    table = ax.table(cellText=summary_df.values, colLabels=summary_df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)  # 禁止自动设置字体大小
    table.set_fontsize(8)  # 减小字体大小以适应更多内容
    table.scale(1.5, 1.5)  # 调整表格大小，第一个参数是列宽的缩放因子，第二个参数是行高的缩放因子
    plt.savefig('summary_df_image.png', dpi=300, bbox_inches='tight')  # 保存为图片

    # 打印DataFrame
    print(summary_df)


with open('./results/integrated_results_iv_BW_2024-05-09_21-48-39.json', 'r') as f:
    data = json.load(f)
    static(data)

