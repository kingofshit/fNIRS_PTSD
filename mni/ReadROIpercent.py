import pandas as pd
roi_num_list = [2, 3, 4, 6, 9, 10, 11, 20, 21, 22, 38, 43, 44, 45, 46, 47, 48]
roi_percent = pd.read_csv('roi_percent.CSV')
roi_sum_list = []
zero_percent_sum_list = []
for item_num in range(roi_percent.shape[0]):
    zero_percent_sum_list.append(0)
roi_percent['percent_sum'] = zero_percent_sum_list
for roi_num in roi_num_list:
    percent_sum = 0
    for item_num in range(roi_percent.shape[0]):
        if roi_num == roi_percent.loc[item_num,'roi_num']:
            percent_sum = percent_sum + roi_percent.loc[item_num,'percentage']
    roi_sum_list.append(percent_sum)
    print(percent_sum)
for roi_num in roi_num_list:
    for item_num in range(roi_percent.shape[0]):
        if roi_num == roi_percent.loc[item_num,'roi_num']:
            roi_percent.loc[item_num, 'percent_sum'] = roi_sum_list[roi_num_list.index(roi_num)]
roi_percent.to_csv('roi_percent_sum.csv',index=0)
print('ok')