from scipy.stats import binom, norm
from math import sqrt
from matplotlib import pyplot as plt
import matplotlib as mpl
import math

mpl.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 输入参数
p0 = 0.10  # 标称次品率
alpha_95 = 0.05  # 95%信度
alpha_90 = 0.10  # 90%信度
# E = 0.05  # 误差限

# 样本量计算公式
def calculate_sample_size(z, p0, E):
    return (z**2 * p0 * (1 - p0)) / (E**2)
def calculate_sample_size1(za, zb, p0, E):
    return (za * zb * sqrt(p0 * (1 - p0))) / E

y1 = []
y2 = []
k1 = []
k2 = []
xx = []
for i in range(1, 20):
    E = i / 1000
    # 单侧检验的标准正态分布的临界值
    z_95_one_sided = norm.ppf(1 - alpha_95)  # 95%信度单侧检验
    z_90_one_sided = norm.ppf(1 - alpha_90)  # 90%信度单侧检验

    # 重新计算样本量
    sample_size_95_one_sided = math.ceil(calculate_sample_size(z_95_one_sided, p0, E))  # 95%信度单侧
    sample_size_90_one_sided = math.ceil(calculate_sample_size(z_90_one_sided, p0, E))  # 90%信度单侧

    # print(sample_size_95_one_sided, sample_size_90_one_sided)
    yy1 = math.ceil(calculate_sample_size1(z_95_one_sided, z_95_one_sided, p0, E))
    yy2 = math.ceil(calculate_sample_size1(z_90_one_sided, z_90_one_sided, p0, E))
    xx.append(E)
    y1.append(yy1)
    y2.append(yy2)
    k1.append(math.ceil(z_95_one_sided * sqrt(p0*(1-p0)) + yy1 * p0))
    k2.append(math.ceil(z_90_one_sided * sqrt(p0*(1-p0)) + yy2 * p0))

print(y1, y2)
print(k1, k2)

# 绘制折线图
# 横坐标为误差限，纵坐标为样本量
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(xx, y1, 'rs--', alpha=0.5, linewidth=1, label='95%')
plt.plot(xx, y2, 'go--', alpha=0.5, linewidth=1, label='90%')

for a, b in zip(xx, y1):
    plt.text(a, b, str(b), ha='center', va='bottom', fontsize=8)
for a, b1 in zip(xx, y2):
    plt.text(a, b1, str(b1), ha='center', va='bottom', fontsize=8)  
plt.legend()
plt.xlabel('δ')
plt.ylabel('样本容量')
plt.title('样本容量与δ的关系')

plt.subplot(1, 2, 2)
plt.plot(xx, k1, 'rs--', alpha=0.5, linewidth=1, label='95%')
plt.plot(xx, k2, 'go--', alpha=0.5, linewidth=1, label='90%')

for a, b in zip(xx, k1):
    plt.text(a, b, str(b), ha='center', va='bottom', fontsize=8)
for a, b1 in zip(xx, k2):
    plt.text(a, b1, str(b1), ha='center', va='bottom', fontsize=8)  
plt.legend()
plt.xlabel('δ')
plt.ylabel('最小检测次数')
plt.title('最小检测次数与δ的关系')

plt.show()