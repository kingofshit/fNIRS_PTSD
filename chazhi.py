import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats


def chazhi(data, PTSDsub_list, HCsub_list):
    oxy_list = ['oxy', 'dxy', 'total']
    isAllNotNAN = 1
    chazhi_table = pd.read_excel('chazhi.xlsx')
    for sub_no in PTSDsub_list + HCsub_list:
        for channel_num in range(1, 49):
            for period_num in range(1, 7):
                for oxy_num in range(1, 4):
                    sub_num = 0
                    for ALLsub_no in PTSDsub_list + HCsub_list:
                        if sub_no == ALLsub_no:
                            break;
                        sub_num += 1
                    label = 'Ch' + str(channel_num) + '_Pr' + str(period_num) + '_' + oxy_list[oxy_num - 1]
                    # 如果数据为空则插值
                    if np.isnan(data.loc[sub_num, label]):
                        isAllNotNAN = 0
                        print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
                        # 寻找周边的通道
                        chazhi_channel_data = []
                        for i in range(4):
                            near_label = 'near' + str(i + 1)
                            if np.isnan(chazhi_table.loc[channel_num - 1, near_label]):
                                continue
                            else:
                                near_channel_num = int(chazhi_table.loc[channel_num - 1, near_label])
                                label_chazhi = 'Ch' + str(near_channel_num) + '_Pr' + str(period_num) + '_' + oxy_list[
                                    oxy_num - 1]
                                # print('--Ch' + str(near_channel_num) + ': ' + str(data.loc[sub_num, label_chazhi]))
                                if not np.isnan(data.loc[sub_num, label_chazhi]):
                                    chazhi_channel_data.append(data.loc[sub_num, label_chazhi])
                        if len(chazhi_channel_data) > 0:
                            print(chazhi_channel_data)
                            print(np.sum(chazhi_channel_data) / len(chazhi_channel_data))
                            data.loc[sub_num, label] = np.sum(chazhi_channel_data) / len(chazhi_channel_data)
    return data, isAllNotNAN

def chazhi_GLM(data, PTSDsub_list, HCsub_list):
    oxy_list = ['oxy', 'dxy', 'total']
    isAllNotNAN = 1
    chazhi_table = pd.read_excel('chazhi.xlsx')
    for sub_no in PTSDsub_list + HCsub_list:
        for channel_num in range(1, 49):
            for beta_num in range(0, 7):
                for oxy_num in range(1, 4):
                    sub_num = 0
                    for ALLsub_no in PTSDsub_list + HCsub_list:
                        if sub_no == ALLsub_no:
                            break;
                        sub_num += 1
                    label = oxy_list[oxy_num-1] + "_beta" + str(beta_num) + "_Ch" + str(channel_num)
                    # print(label)
                    # 如果数据为空则插值
                    if np.isnan(data.loc[sub_num, label]):
                        isAllNotNAN = 0
                        print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
                        # 寻找周边的通道
                        chazhi_channel_data = []
                        for i in range(4):
                            near_label = 'near' + str(i + 1)
                            if np.isnan(chazhi_table.loc[channel_num - 1, near_label]):
                                continue
                            else:
                                near_channel_num = int(chazhi_table.loc[channel_num - 1, near_label])
                                label_chazhi = oxy_list[oxy_num-1] + "_beta" + str(beta_num) + "_Ch" + str(near_channel_num)
                                # print(label_chazhi)
                                if not np.isnan(data.loc[sub_num, label_chazhi]):
                                    chazhi_channel_data.append(data.loc[sub_num, label_chazhi])
                        if len(chazhi_channel_data) > 0:
                            print(chazhi_channel_data)
                            print(np.sum(chazhi_channel_data) / len(chazhi_channel_data))
                            data.loc[sub_num, label] = np.sum(chazhi_channel_data) / len(chazhi_channel_data)
    return data, isAllNotNAN


def feature_chazhi(feature_name):
    PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
    PTSDsub_list = PTSDsub_list.values.tolist()[0]
    HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
    HCsub_list = HCsub_list.values.tolist()[0]
    data = pd.read_csv(feature_name + '.csv', dtype=float)
    while True:
        print('------------------------------------------------------------')
        data, isAllNotNAN = chazhi(data, PTSDsub_list, HCsub_list)
        if isAllNotNAN == 1:
            break
    data.to_csv(feature_name + '_chazhi.csv', index=False)
    print(feature_name + ' done!')


feature_chazhi('mean')
feature_chazhi('integral')
feature_chazhi('variance')
feature_chazhi('skewness')
feature_chazhi('kurtosis')
feature_chazhi('ALFF')
feature_chazhi('fALFF')

# GLM
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
data = pd.read_csv('GLM.csv', dtype=float)
while True:
    print('------------------------------------------------------------')
    data, isAllNotNAN = chazhi_GLM(data, PTSDsub_list, HCsub_list)
    if isAllNotNAN == 1:
        break
data.to_csv('GLM_chazhi.csv', index=False)
print('GLM done!')