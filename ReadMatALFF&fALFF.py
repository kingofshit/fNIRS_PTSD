import scipy.io as scio
import os
import numpy as np
import pandas as pd

ALFF_path = "D:\\fNIRS_Data\\zishu\\ALFF&fALFF\\"
periodlist = ["1RESTING\\","2COUNT\\","3SPEAK\\","4COUNT\\","5LISTEN\\","6COUNT\\"]
Groups = ["HC\\", 'PTSD\\']
oxy_features = ["Oxy\\", "Dxy\\", "Total\\"]
oxy_list = ['oxy', 'dxy', 'total']
ALFF_list = ["ALFF\\", "fALFF\\", "zALFF\\", "zfALFF\\"]
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list

header = ""
ALFF_array = np.zeros((len(Subjects), 6 * 3 * 48, len(ALFF_list)))
for subject in Subjects:
    for period_num in range(0,len(periodlist)):
        for group in Groups:
            for oxy_num in range(0,len(oxy_features)):
                for ALFF_num in range(0,len(ALFF_list)):
                    path = ALFF_path + periodlist[period_num] + group + oxy_features[oxy_num] + ALFF_list[ALFF_num]
                    # print(path)
                    for file in os.walk(path):
                        for filename in file[2]:
                            if filename.split('.')[1] == "mat":
                                if filename.split('.')[0] == subject:
                                    matdata = scio.loadmat(path + filename)
                                    # x = matdata["indexdata"][0][0][7][0]
                                    # print(matdata["indexdata"][0][0][7][0])
                                    for i in range(48):
                                        if Subjects.index(subject) == 0 and ALFF_num == 0:
                                            header = header + "Ch" + str(i + 1) + "_Pr" + str(period_num+1) + "_" + oxy_list[oxy_num] + ','
                                        ALFF_array[Subjects.index(subject), period_num * 3 * 48 + oxy_num * 48 + i, ALFF_num] = \
                                        matdata["indexdata"][0][0][7][0][i]
                                    break
header = header[:-1]
np.savetxt('ALFF.csv', ALFF_array[:,:,0], delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('fALFF.csv', ALFF_array[:,:,1], delimiter=',', header=header, comments='', fmt='%.14f')
print('ok')