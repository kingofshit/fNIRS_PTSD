import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# data = pd.read_csv('mni.csv')
data = pd.read_csv('mni48ch_nihe.csv')
label_list = []

# 创建一个新的3D图像窗口
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 使用scatter函数绘制三维散点图
for i in range(len(data)):
    if data.loc[i, 'region'] == 1:
        print('right')
        x = data.loc[i, 'x']
        y = data.loc[i, 'y']
        z = data.loc[i, 'z']
        ax.scatter(x, y, z, color='red')
        ax.text(x, y, z, str(i+1), size=10, zorder=1, color='k')  # 'k'代表黑色
    elif data.loc[i, 'region'] == 2:
        print('left')
        x = data.loc[i, 'x']
        y = data.loc[i, 'y']
        z = data.loc[i, 'z']
        ax.scatter(x, y, z, color='blue')
        ax.text(x, y, z, str(i+1), size=10, zorder=1, color='k')  # 'k'代表黑色


# 设置坐标轴标签
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# 显示图形
# ax.set_box_aspect([1,1,1])
plt.axis('equal')
plt.show()

print('ok')