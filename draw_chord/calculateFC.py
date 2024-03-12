# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

data = pd.read_csv('../FC_ROI.csv', dtype=float)
PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
sub_list = PTSDsub_list + HCsub_list

oxy_label = 'oxy'
Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']
roi_list = [21,22,38,48,45,46,47,44,10,11,20,6,43,4,2,9,3]

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
    print(Period_name_list[period_num-1])
    PTSD_FC_sum = np.zeros((1, 136))
    HC_FC_sum = np.zeros((1, 136))
    for connection_num in range(0, 136):
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
    PTSDmarix = np.zeros((3, 136*2))
    HCmarix = np.zeros((3, 136*2))
    connection_num = 0
    for i in range(17):
        for j in range(i+1,17):
            PTSDmarix[0,connection_num] = roi_list[i]
            PTSDmarix[1, connection_num] = roi_list[j]
            PTSDmarix[2, connection_num] = PTSD_FC_AVG[0, connection_num]
            PTSDmarix[0, 136*2-connection_num-1] = roi_list[j]
            PTSDmarix[1, 136*2-connection_num-1] = roi_list[i]
            PTSDmarix[2, 136*2-connection_num-1] = PTSD_FC_AVG[0, connection_num]
            HCmarix[0, connection_num] = roi_list[i]
            HCmarix[1, connection_num] = roi_list[j]
            HCmarix[2, connection_num] = HC_FC_AVG[0, connection_num]
            HCmarix[0, 136*2-connection_num-1] = roi_list[j]
            HCmarix[1, 136*2-connection_num-1] = roi_list[i]
            HCmarix[2, 136*2-connection_num-1] = HC_FC_AVG[0, connection_num]
            connection_num +=1
    filename = Period_name_list[period_num-1]+"_FC_ROI.csv"
    np.savetxt("HC_"+filename,HCmarix.T,delimiter=',',comments='',fmt='%.14f')
    np.savetxt("PTSD_"+filename,PTSDmarix.T,delimiter=',',comments='',fmt='%.14f')
print('ok')
