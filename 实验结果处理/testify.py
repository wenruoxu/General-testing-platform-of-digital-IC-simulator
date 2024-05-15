from decimal import Decimal, getcontext

from matplotlib import pyplot as plt

# 设置小数点后的精度
getcontext().prec = 50

k_amount = Decimal('1.95E-2')
y_amount = Decimal('-9.27E-1')
amount = Decimal('4096')
k_N = Decimal('8.21E-5')
y_N = Decimal('-6.95E-1')
N = Decimal('1250')
k_BW = Decimal('6.21E-3')
y_BW = Decimal('8.38E-1')
BW = Decimal('4096')

alpha = k_amount * amount + y_amount
print(alpha)
beta = k_N * N + y_N
print(beta)
gamma = k_BW * BW + y_BW
print(gamma)

result = float(alpha*beta*gamma)
print(result)
#
# result = [float(result1), float(result2), float(result3)]
#
# x = [1250, 2500, 5000]
# value = [14, 27, 53]
#
# # 绘制图表
# plt.figure(figsize=(10, 6))
# plt.plot(x, value, label='Real Value', marker='o', linestyle='-')
# plt.plot(x, result, label='Prediction Result', marker='x', linestyle='--')
#
# plt.title('Real Value and Prediction Result Comparison')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# # plt.grid(True)
# plt.tight_layout()
#
# plt.xscale('log')  # 设置x轴为对数坐标import React from
# plt.yscale('log')  # 设置y轴为对数坐标
#
#
# plt.savefig('simulate_time_comparison.png', dpi=300)  #
# plt.show()
