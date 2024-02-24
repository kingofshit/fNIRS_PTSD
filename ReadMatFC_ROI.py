# coding=gb2312
import scipy.io as scio
import os
import numpy as np
import pandas as pd

FC_path = 'D:\\fNIRS_Data\\zishu\\FC_roi\\'
periodlist = ["1RESTING\\", "2COUNT\\", "3SPEAK\\", "4COUNT\\", "5LISTEN\\", "6COUNT\\"]
# periodlist = ["1RESTING\\", "3SPEAK\\", "5LISTEN\\"]
# periodlist = ["1RESTING\\"]
Groups = ["HC\\", 'PTSD\\']
FC_list = ["zFC_Matrix\\"]
oxy_features = ["Oxy\\", "Dxy\\", "Total\\"]
# oxy_features = ["Oxy\\"]
oxy_list = ['oxy', 'dxy', 'total']
# ALFF_list = ["ALFF\\", "fALFF\\", "zALFF\\", "zfALFF\\"]
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list
roi_percent = pd.read_csv(r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\mni\roi_percent.csv')
roi_name_list = []
for item_num in range(roi_percent.shape[0]):
    item_in_list = 0
    this_roi_name = str(roi_percent.loc[item_num, 'roi_num'])
    for roi_name in roi_name_list:
        if this_roi_name == roi_name:
            item_in_list = 1
            break
    if item_in_list == 0:
        roi_name_list.append(this_roi_name)

header = ""
FC_array = np.zeros((len(Subjects), 6*136*3))
connection2channel = np.zeros((136,3))
for subject in Subjects:
    for period_num in range(0, len(periodlist)):
        for group in Groups:
            for FC_num in range(0, len(FC_list)):
                for oxy_num in range(0, len(oxy_features)):
                    path = FC_path + periodlist[period_num] + group + FC_list[FC_num] + oxy_features[oxy_num]
                    # print(path)
                    for file in os.walk(path):
                        for filename in file[2]:
                            if filename.split('.')[1] == "txt":
                                if filename.split('.')[0] == subject:
                                    # print(path + filename)
                                    data_df = pd.read_csv(path + filename, sep='  ', engine='python', header=None)
                                    data_array = data_df.to_numpy()
                                    connection_num = 0
                                    for i in range(0,17):
                                        for j in range(i+1,17):
                                            FC_array[Subjects.index(subject), period_num*136*3 + connection_num*3 + oxy_num] = data_array [i,j]
                                            if Subjects.index(subject) == 0:
                                                connection2channel[connection_num, 0] = connection_num
                                                connection2channel[connection_num, 1] = i+1
                                                connection2channel[connection_num, 2] = j+1
                                                header = header + "Con" + str(connection_num) + "_Pr" + str(period_num+1) + "_" + oxy_list[oxy_num] + ","
                                            # print('i:' + str(i) + ', j:' + str(j))
                                            connection_num = connection_num + 1
                                    # print(connection_num)

print('ok')
header = header[:-1]
np.savetxt('FC_ROI.csv', FC_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('connection_ROI.csv', connection2channel, delimiter=',', header="connection,ch1,ch2", comments='',fmt='%d')