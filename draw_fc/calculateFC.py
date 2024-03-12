# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

data = pd.read_csv('../FC.csv', dtype=float)
PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
sub_list = PTSDsub_list + HCsub_list

oxy_label = 'oxy'
Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']


def get_FC(data, PTSDsub_list, HCsub_list, sub_no, connection_num, period_num, oxy_label):
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
    label = 'Con' + str(connection_num) + '_Pr' + str(period_num) + '_' + oxy_label

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return data.loc[sub_num, label]

for period_num in range(1,7):
    PTSD_FC_sum = np.zeros((1, 1128))
    HC_FC_sum = np.zeros((1, 1128))
    for connection_num in range(0, 1128):
        for sub_no in PTSDsub_list:
            PTSDdata = get_FC(data, PTSDsub_list, HCsub_list, sub_no, connection_num, period_num, oxy_label)
            PTSD_FC_sum[0,connection_num] += PTSDdata
        for sub_no in HCsub_list:
            HCdata = get_FC(data, PTSDsub_list, HCsub_list, sub_no, connection_num, period_num, oxy_label)
            HC_FC_sum[0,connection_num] += HCdata
    PTSD_FC_AVG = PTSD_FC_sum / len(PTSDsub_list)
    HC_FC_AVG = HC_FC_sum / len(HCsub_list)
    print("ptsd")
    print(PTSD_FC_AVG.max())
    print(PTSD_FC_AVG.min())
    print("hc")
    print(HC_FC_AVG.max())
    print(HC_FC_AVG.min())
    PTSDmarix = np.zeros((48, 48))
    HCmarix = np.zeros((48, 48))
    connection_num = 0
    for i in range(48):
        for j in range(i+1,48):

            PTSDmarix[i,j] = PTSD_FC_AVG[0,connection_num]
            PTSDmarix[j, i] = PTSD_FC_AVG[0, connection_num]
            HCmarix[i, j] = HC_FC_AVG[0,connection_num]
            HCmarix[j, i] = HC_FC_AVG[0, connection_num]
            connection_num +=1
    filename = Period_name_list[period_num-1]+"_FC_CHANNEL.txt"
    np.savetxt("HC_"+filename,HCmarix,delimiter='  ',comments='',fmt='%.14f')
    np.savetxt("PTSD_"+filename,PTSDmarix,delimiter='  ',comments='',fmt='%.14f')
    np.savetxt("SUB_"+filename,HCmarix-PTSDmarix,delimiter='  ',comments='',fmt='%.14f')
print('ok')
