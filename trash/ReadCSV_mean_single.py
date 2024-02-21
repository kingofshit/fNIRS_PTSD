import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from scipy.optimize import curve_fit

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


PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
oxy_list = ['oxy', 'dxy', 'total']
header = ""
savepath = r"C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\plot_data"

oxy_num = 1
period_num = 1
sub_no = "009"

# data = pd.read_csv('../mean.csv', dtype=float)
data = pd.read_csv('../mean_chazhi.csv', dtype=float)
value_array = np.zeros((2, 48))

oxy_label = 'oxy'
for channel_num in range(1, 49):
    header = header + "Ch" + str(channel_num) + ","
    value_array[0,channel_num-1] = get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label)
oxy_label = 'dxy'
for channel_num in range(1, 49):
    value_array[1, channel_num - 1] = get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num,
                                               oxy_label)

header = header[:-1]
np.savetxt(savepath+'\mean_sub'+sub_no+'_pr'+str(period_num)+'.csv', value_array,delimiter=',',header=header,comments='', fmt='%.14f')
print('ok')