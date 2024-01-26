import  pandas as pd
import numpy as np

data = pd.read_excel('chazhi.xlsx')
# print(data)
for i in range(48):
    print(data.loc[i, 'channel'])
    for j in range(4):
        label = 'near' + str(j+1)
        if np.isnan(data.loc[i, label]):
            continue
        else:
            # print(int(data.loc[i, label]))
            isinflag = 0
            for k in range(4):
                label2 = 'near' + str(k + 1)
                if data.loc[int(data.loc[i, label])-1, label2] == data.loc[i, 'channel']:
                    isinflag = 1
            if isinflag == 0:
                print('channel' + str(data.loc[i, 'channel']) + ' not in ' + str(int(data.loc[i, label])))
