import scipy.io as scio
import os
import numpy as np
import pandas as pd

FC_path = 'D:\\fNIRS_Data\\zishu\\FC\\'
# periodlist = ["1RESTING\\", "2COUNT\\", "3SPEAK\\", "4COUNT\\", "5LISTEN\\", "6COUNT\\"]
periodlist = ["1RESTING\\", "3SPEAK\\", "5LISTEN\\"]
# periodlist = ["1RESTING\\"]
Groups = ["HC\\", 'PTSD\\']
FC_list = ["zFC_Matrix\\"]
# oxy_features = ["Oxy\\", "Dxy\\", "Total\\"]
oxy_features = ["Oxy\\"]
oxy_list = ['oxy', 'dxy', 'total']
# ALFF_list = ["ALFF\\", "fALFF\\", "zALFF\\", "zfALFF\\"]
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list


header = ""
FC_array = np.zeros((len(Subjects), 1128*3))
connection2channel = np.zeros((1128,3))
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
                                    for i in range(0,48):
                                        for j in range(i+1,48):
                                            FC_array[Subjects.index(subject), period_num*1128 + connection_num] = data_array [i,j]
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
np.savetxt('FC.csv', FC_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('connection.csv', connection2channel, delimiter=',', header="connection,ch1,ch2", comments='',fmt='%d')