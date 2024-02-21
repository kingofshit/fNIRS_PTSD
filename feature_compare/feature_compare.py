# -*- coding: GBK -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
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

rootdir = r'C:\Users\wjy\OneDrive - hdu.edu.cn\�о���\������\fNIRS_Py'
featrue_compare_list = ['01mean', '02integral', '03variance', '04skewness', '05kurtosis']
result_no = '01'

def find_row_by_content(file_name, target_content, type):
    # type = 0: task
    # type = 1: group
    return_list = []
    if type == 1:
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data_row_number = -1
            for row_number, row in enumerate(reader, start=1):  # �кŴ�1��ʼ����
                if any(target_content in cell for cell in row):
                    # print(f" '{target_content}'λ�ڵ� {row_number} ��")
                    data_row_number = row_number + 2
                if row_number == data_row_number:
                    # print(row)
                    for i in range(1, 4):
                        return_list.append(row[i])
    elif type == 0:
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data_row_number1 = -1
            data_row_number2 = -1
            for row_number, row in enumerate(reader, start=1):  # �кŴ�1��ʼ����
                if any(target_content in cell for cell in row):
                    # print(f" '{target_content}'λ�ڵ� {row_number} ��")
                    data_row_number1 = row_number + 2
                    data_row_number2 = row_number + 3
                if row_number == data_row_number1 or row_number == data_row_number2:
                    # print(row)
                    for i in range(1, 4):
                        return_list.append(row[i])
    return return_list


def draw_bar(values_per_category, categories, label_list, title, figsize):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)  # �Զ���ͼ�δ�С
    bar_width = 1 / (len(values_per_category[0]) + 1)
    index = np.arange(len(categories))
    label_data_pos = np.zeros((len(categories), len(values_per_category[0])))
    data_values = np.linspace(0, 1, len(values_per_category[0]))  # ����һ����0��1���ȷֲ�������
    # ѡ��һ��cmap������ 'viridis'
    cmap_name = 'Wistia'
    cmap = cm.get_cmap(cmap_name)
    # ������ֵӳ�䵽��ɫ
    colors = cmap(data_values)
    # ����������𲢻�������ͼ
    for i in range(len(categories)):
        for j in range(len(values_per_category[i])):
            # print(str(i) + ',' + str(j) + ':  ' + str(values_per_category[i][j]))
            # print(index[i] + bar_width * (j + 1))
            label_data_pos[i, j] = index[i] + bar_width * (j + 1)
            if values_per_category[i][j] > 0:
                plt.text(x=index[i] + bar_width * (j + 1),
                         y=values_per_category[i][j],
                         s=label_list[j], ha='center', va='bottom',
                         fontdict=dict(fontsize=10,
                                       # color='r',
                                       # family='monospace',  # ����,��ѡ'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'
                                       weight='bold',
                                       # ��ֵ����ѡ'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
                                       )  # ������������
                         )
    for j in range(len(values_per_category[i])):
        ax.bar(label_data_pos[:, j], np.array(values_per_category)[:, j], width=bar_width, label=label_list[j],
               color=colors[j])

    # ���� x ��̶ȱ�ǩ��ȷ�����������ζ���
    plt.xticks(index + bar_width * (len(values_per_category[0]) + 1) / 2, categories)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # ֻѡ�������̶�
    # ����x���y�����Ҫ�̶��ߣ��������̶ȱ�ǩ
    plt.tick_params(axis='both', which='major', length=0)
    # ���ñ�����������ǩ
    plt.title(title)
    plt.ylabel('����')
    # # ��ʾͼ��
    # plt.legend(loc='best')
    # # ��ʾͼ��
    # plt.show()
    # ����ͼ��
    plt.savefig('feature_compare'+result_no+'\\'+title + '.jpg')


between_task_array_channel = np.zeros((len(featrue_compare_list),6))
between_group_array_channel= np.zeros((len(featrue_compare_list),3))
between_task_array_roi = np.zeros((len(featrue_compare_list),6))
between_group_array_roi= np.zeros((len(featrue_compare_list),3))
for featrue in featrue_compare_list:
    count_channel_path = rootdir + '\\' + featrue + '\\result' + result_no + '\\' + 'count_channel.csv'
    count_roi_path =  rootdir + '\\' + featrue + '\\result' + result_no + '\\' + 'count_roi.csv'
    print(rootdir + '\\' + featrue + '\\result' + result_no)

    # ��������Ա�
    target = "�������������"
    count_channel = find_row_by_content(count_channel_path, target, 0)
    count_roi = find_row_by_content(count_roi_path, target, 0)
    # print(count_channel)
    # print(count_roi)
    for i in range(6):
        between_task_array_channel[featrue_compare_list.index(featrue), i] = int(float(count_channel[i]))
        between_task_array_roi[featrue_compare_list.index(featrue), i] = int(float(count_roi[i]))

    # ������Ա�
    target = "�����������"
    count_channel = find_row_by_content(count_channel_path, target, 1)
    count_roi = find_row_by_content(count_roi_path, target, 1)
    # print(count_channel)
    # print(count_roi)
    for i in range(3):
        between_group_array_channel[featrue_compare_list.index(featrue), i] = int(float(count_channel[i]))
        between_group_array_roi[featrue_compare_list.index(featrue), i] = int(float(count_roi[i]))

task_header = 'PTSD���t��������,PTSD���t������������̬,PTSD Wilcoxon�����ȼ�������,HC���t��������,HC���t������������̬,HC Wilcoxon�����ȼ�������'
group_header = '��������t��������,��������t������������̬,Mann-Whitney U��������'
if not os.path.exists('feature_compare'+result_no):
    os.mkdir('feature_compare'+result_no)

print(between_task_array_channel)
np.savetxt('feature_compare'+result_no+'\\'+'feature_compare_task_channel_' + result_no + '.csv', between_task_array_channel, delimiter=',', header=task_header, comments='')
categories = ['PTSD���t������������̬', 'PTSD Wilcoxon�����ȼ�������', 'HC���t������������̬', 'HC Wilcoxon�����ȼ�������']
title = '��ͨ������䲻ͬ���������Էֲ�'
roi_plot = between_task_array_channel[:,[1,2,4,5]]
label_list = featrue_compare_list
roi_sum = roi_plot.T
values_per_category = list(roi_sum.tolist())
figsize = (16, 9)
draw_bar(values_per_category, categories, label_list, title, figsize)

print(between_task_array_roi)
np.savetxt('feature_compare'+result_no+'\\'+'feature_compare_task_roi_' + result_no + '.csv', between_task_array_roi, delimiter=',', header=task_header, comments='')
categories = ['PTSD���t������������̬', 'PTSD Wilcoxon�����ȼ�������', 'HC���t������������̬', 'HC Wilcoxon�����ȼ�������']
title = '��ROI����䲻ͬ���������Էֲ�'
roi_plot = between_task_array_roi[:,[1,2,4,5]]
label_list = featrue_compare_list
roi_sum = roi_plot.T
values_per_category = list(roi_sum.tolist())
figsize = (16, 9)
draw_bar(values_per_category, categories, label_list, title, figsize)

print(between_group_array_channel)
np.savetxt('feature_compare'+result_no+'\\'+'feature_compare_group_channel_' + result_no + '.csv', between_group_array_channel, delimiter=',', header=group_header, comments='')
categories = ['��������t������������̬','Mann-Whitney U��������']
title = '��ͨ����䲻ͬ���������Էֲ�'
roi_plot = between_group_array_channel[:,[1,2]]
label_list = featrue_compare_list
roi_sum = roi_plot.T
values_per_category = list(roi_sum.tolist())
figsize = (16, 9)
draw_bar(values_per_category, categories, label_list, title, figsize)


print(between_group_array_roi)
np.savetxt('feature_compare'+result_no+'\\'+'feature_compare_group_roi_' + result_no + '.csv', between_group_array_roi, delimiter=',', header=group_header, comments='')
categories = ['��������t������������̬','Mann-Whitney U��������']
title = '��ROI��䲻ͬ���������Էֲ�'
roi_plot = between_group_array_roi[:,[1,2]]
label_list = featrue_compare_list
roi_sum = roi_plot.T
values_per_category = list(roi_sum.tolist())
figsize = (16, 9)
draw_bar(values_per_category, categories, label_list, title, figsize)