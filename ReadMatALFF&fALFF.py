import scipy.io as scio
import os
import numpy as np
import pandas as pd

Individual_Analysis_Path = "D:\\fNIRS_Data\\zishu\\ALFF&fALFF\\1RESTING\\"
Groups = ["HC\\", 'PTSD\\']
# Groups = ['PTSD\\']
Features = ["Dxy\\", "Oxy\\", "Total\\"]
# Features = ["Dxy\\"]
Betas = ["ALFF\\", "fALFF\\", "zALFF\\", "zfALFF\\"]
# Betas = ["beta_0\\"]

Data = {}
Data.fromkeys(['Group', 'NO.', 'Feature', 'value_Channel1', 'value_Channel2', 'value_Channel3', 'value_Channel4'
, 'value_Channel5', 'value_Channel6', 'value_Channel7', 'value_Channel8', 'value_Channel9', 'value_Channel10'
, 'value_Channel11', 'value_Channel12', 'value_Channel13', 'value_Channel14', 'value_Channel15', 'value_Channel16'
, 'value_Channel17', 'value_Channel18', 'value_Channel19', 'value_Channel20', 'value_Channel21', 'value_Channel22'
, 'value_Channel23', 'value_Channel24', 'value_Channel25', 'value_Channel26', 'value_Channel27', 'value_Channel28'
, 'value_Channel29', 'value_Channel30', 'value_Channel31', 'value_Channel32', 'value_Channel33', 'value_Channel34'
, 'value_Channel35', 'value_Channel36', 'value_Channel37', 'value_Channel38', 'value_Channel39', 'value_Channel40'
, 'value_Channel41', 'value_Channel42', 'value_Channel43', 'value_Channel44', 'value_Channel45', 'value_Channel46'
, 'value_Channel47', 'value_Channel48'])
Data['Group'] = []
Data['NO.'] = []
Data['Feature'] = []
for i in range(48):
    label = 'value_Channel' + str(i+1)
    Data[label] = []

for group in Groups:
    for feature in Features:
        for beta in Betas:
            path = Individual_Analysis_Path + group + feature + beta
            print(path)
            for file in os.walk(path):
                for filename in file[2]:
                    if filename.split('.')[1] == "mat":
                        Data['Group'].append(group)
                        Data['NO.'].append(filename.split('.')[0])
                        Data['Feature'].append(feature + beta)
                        matdata = scio.loadmat(path + filename)
                        for i in range(48):
                            label = 'value_Channel' + str(i + 1)
                            Data[label].append(matdata["indexdata"][0][0][6][0].tolist()[i])

                        # print(path + filename)
                        # matdata = scio.loadmat(path + filename)
                        # print(matdata["indexdata"][0][0][6][0])

xlsx_name = Individual_Analysis_Path + "result.xlsx"
df = pd.DataFrame(Data)  # 创建DataFrame
df.to_excel(xlsx_name, index=False)  # 存表，去除原始索引列（0,1,2...）