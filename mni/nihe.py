import math

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import Axes3D


# 定义椭圆方程
def ellipse_equation(x, a, b, k):
    # return a*x*x+b*x+c
    return b * math.sqrt(math.fabs(1 - (x / a) * (x / a))) + k


# data = pd.read_csv('mni.csv')
data = pd.read_csv('mni48ch.csv')
data_x = []
data_y = []
for i in range(len(data)):
    if data.loc[i, 'z'] == 11:
        data_x.append(data.loc[i, 'x'])
        data_y.append(data.loc[i, 'y'])
        print('11')
data_x = np.array(data_x)
data_y = np.array(data_y)

# 将数据打包成数组形式以便输入到curve_fit
data_points = np.vstack([data_x, data_y]).T
# # 初始猜测值（例如，可能可以根据数据的质心和范围估算初始椭圆中心和半径大小）
# p0 = [np.mean(data_x), np.mean(data_y),  # 初始中心位置猜测
#       max(np.ptp(data_x), np.ptp(data_y)) / 2,  # 初始半径猜测，取x或y轴最大跨度的一半
#       max(np.ptp(data_x), np.ptp(data_y)) / 4]  # 另一个半径猜测，一般较小

# 使用curve_fit拟合椭圆参数
params, covariance = curve_fit(ellipse_equation, data_points[:, 0], data_points[:, 1])

# 得到拟合后的参数
a, b, k = params

# 绘制拟合的椭圆
ellipse = Ellipse((0, k), 2 * a, 2 * b, edgecolor='r', facecolor='none', label='拟合椭圆')
plt.gca().add_patch(ellipse)

plt.legend()
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('散点拟合椭圆')
plt.show()

# # 创建一个新的3D图像窗口
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # 使用scatter函数绘制三维散点图
# for i in range(len(data)):
#     if data.loc[i, 'region'] == 1:
#         print('right')
#         x = data.loc[i, 'x']
#         y = data.loc[i, 'y']
#         z = data.loc[i, 'z']
#         ax.scatter(x, y, z, color='red')
#     elif data.loc[i, 'region'] == 2:
#         print('left')
#         x = data.loc[i, 'x']
#         y = data.loc[i, 'y']
#         z = data.loc[i, 'z']
#         ax.scatter(x, y, z, color='blue')
#
# # 设置坐标轴标签
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
#
# # 显示图形
# plt.show()


print('ok')
