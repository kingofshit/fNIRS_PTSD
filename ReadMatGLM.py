import scipy.io as scio
import os
import numpy as np
import pandas as pd

Individual_Analysis_Path = "D:\\fNIRS_Data\\zishu\\NIRS_KIT_Individual_Analysis\\"
Groups = ["HC\\", 'PTSD\\']
# Groups = ['PTSD\\']
oxy_features = ["Oxy\\", "Dxy\\", "Total\\"]
oxy_list = ['oxy', 'dxy', 'total']
# Features = ["Dxy\\"]
Betas = ["beta_0\\", "beta_1\\", "beta_2\\", "beta_3\\", "beta_4\\", "beta_5\\", "beta_6\\"]
# Betas = ["beta_0\\"]
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list

header = ""
GLM_array = np.zeros((len(Subjects), 3 * 7 * 48))
for subject in Subjects:
    print(subject)
    for group in Groups:
        for oxy_num in range(0,len(oxy_features)):
            for beta_num in range(0,len(Betas)):
                path = Individual_Analysis_Path + group + oxy_features[oxy_num] + Betas[beta_num]
                for file in os.walk(path):
                    for filename in file[2]:
                        if filename.split('.')[1] == "mat":
                            if filename.split('.')[0] == subject:
                                # print(path)
                                matdata = scio.loadmat(path + filename)
                                for i in range(48):
                                    if Subjects.index(subject) == 0:
                                        header = header + oxy_list[oxy_num] + "_beta" + str(beta_num) + "_Ch" + str(i+1) + ','
                                    GLM_array[Subjects.index(subject), oxy_num * 7 * 48 + beta_num * 48 + i] = matdata["indexdata"][0][0][6][0].tolist()[i]

header = header[:-1]
np.savetxt('GLM.csv', GLM_array, delimiter=',', header=header, comments='', fmt='%.14f')