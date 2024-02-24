import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
import matplotlib.ticker as ticker
import os

config = {
    "font.family": 'serif',
    "font.size": 10,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

if_draw = 0
PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
oxy_list = ['oxy', 'dxy', 'total']
Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']
sub_list = PTSDsub_list + HCsub_list
channel_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                41, 42, 43, 44, 45, 46, 47, 48]

roi_table = pd.read_csv(r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\mni\roi.csv')
roi_name_list = roi_table.columns.tolist()


def draw_heatmap(data, xticks_labels, yticks_labels, title):
    if if_draw == 1:
        fig, ax = plt.subplots(figsize=(20, 4), dpi=300)
        # plt.figure(figsize=(10, 10), dpi=100)
        cmap = 'Reds_r'  # 你可以选择不同的颜色映射方案
        ax.imshow(data, cmap=cmap)
        ax.set_title(title, fontsize=15, y=1.05)
        # 在每个单元格中心位置添加数值标签
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if data[i, j] < 0.05:
                    text_val = format(data[i, j], '.3f')  # 格式化数值
                    ax.text(j, i, text_val, ha="center", va="center", color="w")
        # 设置坐标轴标题
        plt.xlabel('通道')
        plt.ylabel('任务')
        # 设置坐标轴标签
        x_position = range(len(xticks_labels))
        plt.xticks(x_position, xticks_labels)
        plt.xticks(rotation=45)
        y_position = range(len(yticks_labels))
        plt.yticks(y_position, yticks_labels)
        # 隐藏x轴和y轴的主要刻度线，但保留刻度标签
        plt.tick_params(axis='both', which='major', length=0)
        # # 添加colorbar
        # plt.colorbar(pad=0.2, shrink=0.6)
        plt.subplots_adjust(left=0.05, right=0.95)  # 左侧留白为15%，右侧留白为10%
        # # 显示图形
        # plt.show()
        # 保存图像
        plt.savefig('channel_' + title + '.jpg')


def draw_bar(values_per_category, categories, label_list, title, figsize):
    if if_draw == 1:
        fig, ax = plt.subplots(figsize=figsize, dpi=300)  # 自定义图形大小
        bar_width = 1 / (len(values_per_category[0]) + 1)
        index = np.arange(len(categories))
        label_data_pos = np.zeros((len(categories), len(values_per_category[0])))
        data_values = np.linspace(0, 1, len(values_per_category[0]))  # 创建一个从0到1均匀分布的数组
        # 选择一个cmap，例如 'viridis'
        cmap_name = 'Wistia'
        cmap = cm.get_cmap(cmap_name)
        # 将数据值映射到颜色
        colors = cmap(data_values)
        # 遍历所有类别并绘制条形图
        for i in range(len(categories)):
            for j in range(len(values_per_category[i])):
                # print(str(i) + ',' + str(j) + ':  ' + str(values_per_category[i][j]))
                # print(index[i] + bar_width * (j + 1))
                label_data_pos[i, j] = index[i] + bar_width * (j + 1)
                if values_per_category[i][j] > 0:
                    plt.text(x=index[i] + bar_width * (j + 1),
                             y=values_per_category[i][j],
                             s=label_list[j], ha='center', va='bottom',
                             fontdict=dict(fontsize=12,
                                           # color='r',
                                           # family='monospace',  # 字体,可选'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'
                                           weight='bold',
                                           # 磅值，可选'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
                                           )  # 字体属性设置
                             )
        for j in range(len(values_per_category[i])):
            ax.bar(label_data_pos[:, j], np.array(values_per_category)[:, j], width=bar_width, label=label_list[j],
                   color=colors[j])

        # 设置 x 轴刻度标签，确保它们与条形对齐
        plt.xticks(index + bar_width * (len(values_per_category[0]) + 1) / 2, categories)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # 只选择整数刻度
        # 隐藏x轴和y轴的主要刻度线，但保留刻度标签
        plt.tick_params(axis='both', which='major', length=0)
        # 设置标题和坐标轴标签
        plt.title(title)
        plt.ylabel('数量')
        # # 显示图例
        # plt.legend(loc='best')
        # # 显示图形
        # plt.show()
        # 保存图像
        plt.savefig('channel_' + title + '.jpg')


def between_task():
    result_data = pd.read_csv('result_channel.csv', dtype=float)
    # 存储PTSD结果
    oxy_sum = np.zeros((3, 3))
    channel_sum = np.zeros((48, 3))
    roi_sum = np.zeros((len(roi_name_list), 3))
    period_sum = np.zeros((6, 3))
    # 存储HC结果
    oxy_sum2 = np.zeros((3, 3))
    channel_sum2 = np.zeros((48, 3))
    roi_sum2 = np.zeros((len(roi_name_list), 3))
    period_sum2 = np.zeros((6, 3))

    for plot_oxy_type in [1, 2, 3]:
        for i in range(0, result_data.shape[0]):
            oxytype = result_data.iat[i, 0]
            channel = result_data.iat[i, 1]
            period1 = result_data.iat[i, 2]
            period2 = result_data.iat[i, 3]
            PTSDperiod1_test_pvalue = result_data.iat[i, 4]
            PTSDperiod2_test_pvalue = result_data.iat[i, 5]
            PTSD_p_value = result_data.iat[i, 6]
            PTSD_mannwhitneyu_p_value = result_data.iat[i, 7]
            HCperiod1_test_pvalue = result_data.iat[i, 8]
            HCperiod2_test_pvalue = result_data.iat[i, 9]
            HC_p_value = result_data.iat[i, 10]
            HC_mannwhitneyu_p_value = result_data.iat[i, 11]

            oxy_label = oxy_list[int(oxytype) - 1]
            for roi_num in range(0, len(roi_name_list)):
                roi_name = roi_name_list[roi_num]
                for roi_channel in roi_table[roi_name]:
                    if not np.isnan(roi_channel):
                        if int(roi_channel) == int(channel):
                            # print(str(roi_num)+roi_name)
                            roi = roi_num + 1

            if int(oxytype) == plot_oxy_type:
                if PTSD_p_value < 0.05:
                    oxy_sum[plot_oxy_type - 1, 0] += 1
                    channel_sum[int(channel) - 1, 0] += 1
                    roi_sum[int(roi - 1), 0] += 1
                    period_sum[int(period1) - 1, 0] += 1
                    period_sum[int(period2) - 1, 0] += 1
                    if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                        oxy_sum[plot_oxy_type - 1, 1] += 1
                        channel_sum[int(channel) - 1, 1] += 1
                        roi_sum[int(roi - 1), 1] += 1
                        period_sum[int(period1) - 1, 1] += 1
                        period_sum[int(period2) - 1, 1] += 1
                        print('- PTSD配对t检验显著： ' + oxy_label + '_' + str(channel) + '_' + Period_name_list[
                            int(period1) - 1] + '_' + Period_name_list[int(period2) - 1] + ': ' + str(
                            PTSD_p_value))
                if PTSD_mannwhitneyu_p_value < 0.05:
                    oxy_sum[plot_oxy_type - 1, 2] += 1
                    channel_sum[int(channel) - 1, 2] += 1
                    roi_sum[int(roi - 1), 2] += 1
                    period_sum[int(period1) - 1, 2] += 1
                    period_sum[int(period2) - 1, 2] += 1

                if HC_p_value < 0.05:
                    oxy_sum2[plot_oxy_type - 1, 0] += 1
                    channel_sum2[int(channel) - 1, 0] += 1
                    roi_sum2[int(roi - 1), 0] += 1
                    period_sum2[int(period1) - 1, 0] += 1
                    period_sum2[int(period2) - 1, 0] += 1
                    if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                        oxy_sum2[plot_oxy_type - 1, 1] += 1
                        channel_sum2[int(channel) - 1, 1] += 1
                        roi_sum2[int(roi - 1), 1] += 1
                        period_sum2[int(period1) - 1, 1] += 1
                        period_sum2[int(period2) - 1, 1] += 1
                        print('- HC配对t检验显著： ' + oxy_label + '_' + str(channel) + '_' + Period_name_list[
                            int(period1) - 1] + '_' + Period_name_list[int(period2) - 1] + ': ' + str(
                            HC_p_value))
                if HC_mannwhitneyu_p_value < 0.05:
                    oxy_sum2[plot_oxy_type - 1, 2] += 1
                    channel_sum2[int(channel) - 1, 2] += 1
                    roi_sum2[int(roi - 1), 2] += 1
                    period_sum2[int(period1) - 1, 2] += 1
                    period_sum2[int(period2) - 1, 2] += 1

    with open("count_channel.txt", "w") as file:
        file.write("分通道结果,\n")
        file.write("任务间总显著性,\n")
        file.write("类别,配对t检验显著,配对t检验显著且正态,Wilcoxon符号秩检验显著," + "\n")
        file.write('PSTD,' + str(sum(oxy_sum[i, 0] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum[i, 1] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum[i, 2] for i in range(0, 3))) + ',\n')
        file.write('HC,' + str(sum(oxy_sum2[i, 0] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum2[i, 1] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum2[i, 2] for i in range(0, 3))) + ',\n')

    categories = ['配对t检验显著', '配对t检验显著且正态', 'Wilcoxon符号秩检验显著']
    title = '任务间不同血红蛋白显著性分布'
    oxy_plot = np.zeros((6, 3))
    label_list = []
    for i in range(0, 3):
        oxy_plot[i * 2, :] = oxy_sum[i, :]
        oxy_plot[i * 2 + 1, :] = oxy_sum2[i, :]
        label_list.append('PTSD_' + oxy_list[i])
        label_list.append('HC_' + oxy_list[i])
    oxy_sum = oxy_plot.T
    values_per_category = list(oxy_sum.tolist())
    figsize = (15, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,配对t检验显著,配对t检验显著且正态,Wilcoxon符号秩检验显著," + "\n")
        for i in range(0, oxy_plot.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, oxy_plot.shape[1]):
                file.write(str(oxy_plot[i, j])+',')
            file.write("\n")


    categories = ['配对t检验显著', '配对t检验显著且正态', 'Wilcoxon符号秩检验显著']
    title = '任务间不同通道显著性分布'
    channel_plot = np.zeros((96, 3))
    label_list = []
    for i in range(0, 48):
        channel_plot[i * 2, :] = channel_sum[i, :]
        channel_plot[i * 2 + 1, :] = channel_sum2[i, :]
        label_list.append('PTSD_' + str(i + 1))
        label_list.append('HC_' + str(i + 1))
    channel_sum = channel_plot.T
    values_per_category = list(channel_sum.tolist())
    figsize = (80, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,配对t检验显著,配对t检验显著且正态,Wilcoxon符号秩检验显著," + "\n")
        for i in range(0, channel_plot.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, channel_plot.shape[1]):
                file.write(str(channel_plot[i, j])+',')
            file.write("\n")


    categories = ['配对t检验显著', '配对t检验显著且正态', 'Wilcoxon符号秩检验显著']
    title = '任务间不同ROI显著性分布'
    roi_plot = np.zeros((len(roi_name_list)*2, 3))
    label_list = []
    for i in range(0, len(roi_name_list)):
        roi_plot[i * 2, :] = roi_sum[i, :]
        roi_plot[i * 2 + 1, :] = roi_sum2[i, :]
        label_list.append('PTSD_' + roi_name_list[i])
        label_list.append('HC_' + roi_name_list[i])
    roi_sum = roi_plot.T
    values_per_category = list(roi_sum.tolist())
    figsize = (35, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,配对t检验显著,配对t检验显著且正态,Wilcoxon符号秩检验显著," + "\n")
        for i in range(0, roi_plot.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, roi_plot.shape[1]):
                file.write(str(roi_plot[i, j])+',')
            file.write("\n")

    categories = ['配对t检验显著', '配对t检验显著且正态', 'Wilcoxon符号秩检验显著']
    title = '任务间不同任务阶段显著性分布'
    period_plot = np.zeros((12, 3))
    label_list = []
    for i in range(0, 6):
        period_plot[i * 2, :] = period_sum[i, :]
        period_plot[i * 2 + 1, :] = period_sum2[i, :]
        label_list.append('PTSD_' + Period_name_list[i])
        label_list.append('HC_' + Period_name_list[i])
    period_sum = period_plot.T
    values_per_category = list(period_sum.tolist())
    figsize = (30, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,配对t检验显著,配对t检验显著且正态,Wilcoxon符号秩检验显著," + "\n")
        for i in range(0, period_plot.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, period_plot.shape[1]):
                file.write(str(period_plot[i, j])+',')
            file.write("\n")


def between_group():
    # 组间
    oxy_sum = np.zeros((3, 3))
    channel_connection_sum = np.zeros((136, 3))
    period_sum = np.zeros((6, 3))
    for plot_oxy_type in [1, 2, 3]:
        group_result_data = pd.read_csv('result_group_channel.csv', dtype=float)
        # plot_t_data = np.zeros((6, 48))
        # plot_mannwhitneyu_data = np.zeros((6, 48))
        for i in range(0, group_result_data.shape[0]):
            oxytype = group_result_data.iat[i, 0]
            channel_connnection = group_result_data.iat[i, 1]
            period = group_result_data.iat[i, 2]
            PTSD_test_pvalue = group_result_data.iat[i, 3]
            HC_test_pvalue = group_result_data.iat[i, 4]
            t_p_value = group_result_data.iat[i, 5]
            mannwhitneyu_p_value = group_result_data.iat[i, 6]

            oxy_label = oxy_list[int(oxytype) - 1]
            # channel_name = channel_list[int(channel - 1)]

            if int(oxytype) == plot_oxy_type:
                if t_p_value < 0.05:
                    oxy_sum[plot_oxy_type - 1, 0] += 1
                    channel_connection_sum[int(channel_connnection), 0] += 1
                    period_sum[int(period) - 1, 0] += 1
                    if PTSD_test_pvalue > 0.05 and HC_test_pvalue > 0.05:
                        oxy_sum[plot_oxy_type - 1, 1] += 1
                        channel_connection_sum[int(channel_connnection), 1] += 1
                        period_sum[int(period) - 1, 1] += 1
                        print('- 独立样本t检验显著： ' + oxy_label + '_' + str(channel_connnection) + '_' + Period_name_list[
                            int(period) - 1] + ': ' + str(t_p_value))
                if mannwhitneyu_p_value < 0.05:
                    oxy_sum[plot_oxy_type - 1, 2] += 1
                    channel_connection_sum[int(channel_connnection), 2] += 1
                    period_sum[int(period) - 1, 2] += 1
                    print('- mannwhitney u检验显著： ' + oxy_label + '_' + str(channel_connnection) + '_' + Period_name_list[
                        int(period) - 1] + ': ' + str(mannwhitneyu_p_value))
                # plot_t_data[int(period) - 1, channel_name - 1] = t_p_value
                # plot_mannwhitneyu_data[int(period) - 1, channel_name - 1] = mannwhitneyu_p_value

        # plot_t_roi = np.zeros((6, 48))
        # plot_mannwhitneyu_roi = np.zeros((6, 48))
        # roi_channel_num = 0
        # roi_channel_list = []
        # for roi_num in range(0, len(roi_name_list)):
        #     roi_name = roi_name_list[roi_num]
        #     for roi_channel in roi_table[roi_name]:
        #         if not np.isnan(roi_channel):
        #             plot_t_roi[:, roi_channel_num] = plot_t_data[:, int(roi_channel) - 1]
        #             plot_mannwhitneyu_roi[:, roi_channel_num] = plot_mannwhitneyu_data[:, int(roi_channel) - 1]
        #             roi_channel_num += 1
        #             roi_channel_list.append(int(roi_channel))

        # xticks_labels = roi_channel_list
        # yticks_labels = Period_name_list
        # title = oxy_list[int(plot_oxy_type) - 1] + '  独立样本t检验'
        # draw_heatmap(plot_t_roi, xticks_labels, yticks_labels, title)
        # title = oxy_list[int(plot_oxy_type) - 1] + '  Mann-Whitney U检验'
        # draw_heatmap(plot_mannwhitneyu_roi, xticks_labels, yticks_labels, title)

    print(oxy_sum)
    categories = ['独立样本t检验显著', '独立样本t检验显著且正态', 'Mann-Whitney U检验显著']
    title = '组间不同血红蛋白显著性分布'
    oxy_sum = oxy_sum.T
    label_list = oxy_list
    values_per_category = list(oxy_sum.tolist())
    figsize = (10, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write("组间总显著性,\n")
        file.write("类别,独立样本t检验显著,独立样本t检验显著且正态,Mann-Whitney U检验显著," + "\n")
        file.write('PSTD+HC,' + str(sum(oxy_sum.T[i, 0] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum.T[i, 1] for i in range(0, 3))) + ','
                   + str(sum(oxy_sum.T[i, 2] for i in range(0, 3))) + ',\n')
        file.write(title + ",\n")
        file.write("类别,独立样本t检验显著,独立样本t检验显著且正态,Mann-Whitney U检验显著," + "\n")
        for i in range(0, oxy_sum.T.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, oxy_sum.T.shape[1]):
                file.write(str(oxy_sum.T[i, j])+',')
            file.write("\n")

    # print(channel_sum)
    categories = ['独立样本t检验显著', '独立样本t检验显著且正态', 'Mann-Whitney U检验显著']
    title = '组间不同通道连接显著性分布'
    channel_sum = channel_connection_sum.T
    label_list = list(range(1, 137))
    values_per_category = list(channel_sum.tolist())
    figsize = (50, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,独立样本t检验显著,独立样本t检验显著且正态,Mann-Whitney U检验显著," + "\n")
        for i in range(0, channel_sum.T.shape[0]):
            file.write(str(label_list[i])+',')
            for j in range(0, channel_sum.T.shape[1]):
                file.write(str(channel_sum.T[i, j])+',')
            file.write("\n")

    # print(roi_sum)
    # categories = ['独立样本t检验显著', '独立样本t检验显著且正态', 'Mann-Whitney U检验显著']
    # title = '组间不同ROI显著性分布'
    # roi_sum = roi_sum.T
    # label_list = roi_name_list
    # values_per_category = list(roi_sum.tolist())
    # figsize = (26, 6)
    # draw_bar(values_per_category, categories, label_list, title, figsize)
    # with open("count_channel.txt", "a") as file:
    #     file.write(title + ",\n")
    #     file.write("类别,独立样本t检验显著,独立样本t检验显著且正态,Mann-Whitney U检验显著," + "\n")
    #     for i in range(0, roi_sum.T.shape[0]):
    #         file.write(label_list[i]+',')
    #         for j in range(0, roi_sum.T.shape[1]):
    #             file.write(str(roi_sum.T[i, j])+',')
    #         file.write("\n")

    print(period_sum)
    categories = ['独立样本t检验显著', '独立样本t检验显著且正态', 'Mann-Whitney U检验显著']
    title = '组间不同任务阶段显著性分布'
    period_sum = period_sum.T
    label_list = Period_name_list
    values_per_category = list(period_sum.tolist())
    figsize = (20, 6)
    draw_bar(values_per_category, categories, label_list, title, figsize)
    with open("count_channel.txt", "a") as file:
        file.write(title + ",\n")
        file.write("类别,独立样本t检验显著,独立样本t检验显著且正态,Mann-Whitney U检验显著," + "\n")
        for i in range(0, period_sum.T.shape[0]):
            file.write(label_list[i]+',')
            for j in range(0, period_sum.T.shape[1]):
                file.write(str(period_sum.T[i, j])+',')
            file.write("\n")


# between_task()
between_group()


# 获取当前工作目录
current_dir = os.getcwd()

# 旧文件名和新文件名
old_file = os.path.join(current_dir, 'count_channel.txt')
new_file = os.path.join(current_dir, 'count_channel.csv')

# 先检查新文件是否存在并删除（强制覆盖）
if os.path.exists(new_file):
    os.remove(new_file)
# 使用os.rename()进行重命名
os.rename(old_file, new_file)

print('ok')
