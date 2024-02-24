import os
import numpy as np
import pandas as pd
from scipy import stats

Network_path = 'D:\\fNIRS_Data\\zishu\\Gretna\\'
periodlist = ["1RESTING\\", "3SPEAK\\", "5LISTEN\\"]
Groups = ["HC\\", 'PTSD\\']
Network_single_featrue_list = ['Assortativity\\ar.txt', 'Hierarchy\\ab.txt', 'NetworkEfficiency\\aEg.txt',
                               'NetworkEfficiency\\aEloc.txt', 'SmallWorld\\aCp.txt', 'SmallWorld\\aGamma.txt',
                               'SmallWorld\\aLambda.txt', 'SmallWorld\\aLp.txt', 'SmallWorld\\aSigma.txt',
                               'Synchronization\\as.txt']
Network_multiple_featrue_list = ['RichClub\\phi_real_Thres001.txt']

PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list
All_PTSDsub = ['006', '007', '008', '009', '010', '011', '012', '013', '014', '015',
               '016', '017', '018', '019', '020', '046', '047', '048', '049', '051',
               '053', '054', '055', '056', '059', '060', '061', '062', '063', '064',
               '065', '066', '084', '085']
All_HCsub = ['004', '005', '021', '022', '023', '024', '025', '026', '027', '028',
             '029', '030', '031', '032', '033', '034', '035', '037', '038', '039',
             '040', '041', '042', '043', '044', '045', '057', '058', '067', '068',
             '069', '070', '071', '072', '073', '074', '075', '076', '077', '078',
             '079', '080', '081', '082', '083']

header = "1RESTING,3SPEAK,5LISTEN"
Network_single_featrue_array = np.zeros((len(Network_single_featrue_list), len(Subjects), 3))
# Hierarchy_ab_array = np.zeros((len(Subjects), 3))
# NetworkEfficiency_aEg_array = np.zeros((len(Subjects), 3))
# NetworkEfficiency_aEloc_array = np.zeros((len(Subjects), 3))
# SmallWorld_aCp_array = np.zeros((len(Subjects), 3))
# SmallWorld_aGamma_array = np.zeros((len(Subjects), 3))
# SmallWorld_aLambda_array = np.zeros((len(Subjects), 3))
# SmallWorld_aLp_array = np.zeros((len(Subjects), 3))
# SmallWorld_aSigma_array = np.zeros((len(Subjects), 3))
# Synchronization_as_array = np.zeros((len(Subjects), 3))

for period_num in range(0, len(periodlist)):
    for group in Groups:
        for Network_single_featrue_num in range(0,len(Network_single_featrue_list)):
            path = Network_path + periodlist[period_num] + group + Network_single_featrue_list[
                Network_single_featrue_num]
            # print(path)
            data_df = pd.read_csv(path, sep='  ', engine='python', header=None)
            data_array = data_df.to_numpy()

            if group == "HC\\":
                for subject in HCsub_list:
                    sub_num = All_HCsub.index(subject)
                    Network_single_featrue_array[Network_single_featrue_num, Subjects.index(subject), period_num] \
                        = data_array[sub_num, 0]
            elif group == "PTSD\\":
                for subject in PTSDsub_list:
                    sub_num = All_PTSDsub.index(subject)
                    Network_single_featrue_array[Network_single_featrue_num, Subjects.index(subject), period_num] \
                        = data_array[sub_num, 0]

for Network_single_featrue_num in range(0,len(Network_single_featrue_list)):
    csv_name = Network_single_featrue_list[Network_single_featrue_num].replace('\\','_').replace('.txt','.csv')
    print(csv_name)
    for period_num in range(0, len(periodlist)):
        data = Network_single_featrue_array[Network_single_featrue_num, :, period_num]
        Network_single_featrue_array[Network_single_featrue_num, :, period_num] = stats.zscore(data)
    np.savetxt('10Network\\'+csv_name, Network_single_featrue_array[Network_single_featrue_num,:,:], delimiter=',', header=header, comments='', fmt='%.14f')
    print(Network_single_featrue_array[Network_single_featrue_num,:,:])
print('ok')