# -*- coding: GBK -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

rootdir = r'C:\Users\wjy\OneDrive - hdu.edu.cn\�о���\������\fNIRS_Py'
featrue_compare_list = ['01mean', '02integral', '03variance', '04skewness', '05kurtosis', '06GLM']
result_no = '01'


def find_row_by_content(file_name, target_content):
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader, start=1):  # �кŴ�1��ʼ����
            if any(target_content in cell for cell in row):
                print(f" '{target_content}'λ�ڵ� {row_number} ��")
                # print(row)
                return row_number  # �����ҵ���Ŀ���к�
    return None  # ���δ�ҵ�Ŀ�����ݣ��򷵻�None

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
    row_num_channel = find_row_by_content(count_channel_path, target)
    row_num_roi = find_row_by_content(count_roi_path, target)

    # ������Ա�
    target = "�����������"
    row_num = find_row_by_content(count_channel_path, target)
    row_num_roi = find_row_by_content(count_roi_path, target)
