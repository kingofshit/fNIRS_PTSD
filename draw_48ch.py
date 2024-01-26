import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from scipy.optimize import curve_fit
from scipy.interpolate import interp2d


def get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label):
    # channel_num   1-48
    # period_num   1:RESTING, 2:COUNT, 3:SPEAK, 4:COUNT, 5:LISTEN, 6:COUNT
    # oxy_num   1:OXY, 2:DXY, 3:TOTAL
    # 读取 CSV 文件

    # 生成标签
    sub_num = 0
    for ALLsub_no in PTSDsub_list + HCsub_list:
        if sub_no == ALLsub_no:
            break;
        sub_num += 1
    label = 'Ch' + str(channel_num) + '_Pr' + str(period_num) + '_' + oxy_label

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return data.loc[sub_num, label]


def avg_neighbors(array, index):
    # 获取数组的形状
    rows, cols = array.shape

    # 检查给定的索引是否有效
    if not (0 <= index[0] < rows and 0 <= index[1] < cols):
        raise ValueError("Invalid index")

    # 计算给定元素周围邻居的平均值
    neighbors = []
    if index[0] > 0:
        neighbors.append(array[index[0] - 1, index[1]])
    if index[0] < rows - 1:
        neighbors.append(array[index[0] + 1, index[1]])
    if index[1] > 0:
        neighbors.append(array[index[0], index[1] - 1])
    if index[1] < cols - 1:
        neighbors.append(array[index[0], index[1] + 1])

    # 过滤掉无效值（如NaN）
    valid_neighbors = [n for n in neighbors if not np.isnan(n)]

    # 如果没有有效的邻居，则返回None
    if not valid_neighbors:
        return np.nan

    # 计算平均值并返回结果
    return np.mean(valid_neighbors)


channels = [
    [np.nan, 1, np.nan, 3, np.nan, 4, np.nan, 6, np.nan, 7, np.nan, 9, np.nan, 10, np.nan, 12, np.nan, 13, np.nan, 15,
     np.nan],
    [2, np.nan, 17, np.nan, 5, np.nan, 21, np.nan, 8, np.nan, 25, np.nan, 11, np.nan, 29, np.nan, 14, np.nan, 33,
     np.nan, 16],
    [np.nan, 18, np.nan, 19, np.nan, 22, np.nan, 23, np.nan, 26, np.nan, 27, np.nan, 30, np.nan, 31, np.nan, 34, np.nan,
     35, np.nan],
    [np.nan, np.nan, 20, np.nan, 37, np.nan, 24, np.nan, 40, np.nan, 28, np.nan, 43, np.nan, 32, np.nan, 46, np.nan, 36,
     np.nan, np.nan],
    [np.nan, np.nan, np.nan, 38, np.nan, 39, np.nan, 41, np.nan, 42, np.nan, 44, np.nan, 45, np.nan, 47, np.nan, 48,
     np.nan, np.nan, np.nan]]
PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
oxy_list = ['oxy', 'dxy', 'total']
draw_sub = ["066"]

# data = pd.read_csv('mean.csv', dtype=float)
data = pd.read_csv('mean_chazhi.csv', dtype=float)
for oxy_num in range(1, 4):
    oxy_label = oxy_list[oxy_num - 1]
    for sub_no in draw_sub:
        values = np.zeros((6, 5, 21))
        for period_num in range(1, 7):
            values[period_num - 1, :, :] = channels
            for channel_num in range(1, 49):
                for i in range(0, 5):
                    for j in range(0, 21):
                        if values[period_num - 1][i][j] == channel_num:
                            present_data = get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num,
                                                    oxy_label)
                            values[period_num - 1][i][j] = present_data
        value_min = np.nanmin(values)
        value_max = np.nanmax(values)

        # 画图
        Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']
        fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 4))
        plt.rcParams.update({'font.size': 10})
        for draw_num in range(0, 6):
            array = values[draw_num]

            # 插值
            for i in range(0, 5):
                for j in range(0, 21):
                    if np.isnan(array[i][j]):
                        array[i][j] = avg_neighbors(array, (i, j))
            # 定义插值函数
            # interp = interp2d(np.arange(21), np.arange(5), data, kind='linear')
            interp = interp2d(np.arange(21), np.arange(5), array, kind='cubic')
            # 生成新的插值数据矩阵
            new_data = interp(np.linspace(0, 20, 210), np.linspace(0, 4, 50))
            # 绘制热力图
            image = axs[draw_num // 3, draw_num % 3].imshow(new_data, cmap='jet', vmin=value_min, vmax=value_max)
            axs[draw_num // 3, draw_num % 3].set_title(Period_name_list[draw_num])
            axs[draw_num // 3, draw_num % 3].axis('off')

            # # 不插值
            # image = axs[draw_num // 3, draw_num % 3].imshow(array, cmap='jet', vmin=value_min, vmax=value_max)
            # axs[draw_num // 3, draw_num % 3].set_title(Period_name_list[draw_num])
            # axs[draw_num // 3, draw_num % 3].axis('off')

        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.9, 0.2, 0.03, 0.6])
        cb = fig.colorbar(image, cax=cbar_ax, orientation='vertical')
        cb.set_label(oxy_label)

        # 显示图形
        plt.show()

        # # 保存图像
        # output_path = 'figs/mean_not_chazhi/' + oxy_label + '/HC/'
        # if not os.path.exists(output_path):
        #     os.makedirs(output_path)
        # plt.savefig(output_path + sub_no + '.png', dpi=300)
        # print(output_path + sub_no + '.png')
