"""
FILE NAME: generate_random.py
DATE: 2024/5/8 上午10:02
AUTHOR: Wen Ruoxu

NOTE:
    
"""

import random

def generate_rom_data(bit_width, num_lines, filename='./rom_data.txt'):
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            # 生成一个随机数，并转换为指定位宽的二进制字符串
            data = bin(random.getrandbits(bit_width))[2:].zfill(bit_width)
            file.write(data + '\n')

if __name__ == '__main__':
    bit_width = 32  # 指定位宽
    num_lines = 4096  # 指定数据行数
    generate_rom_data(bit_width, num_lines)
