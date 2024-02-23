import statsmodels.stats.multitest as smm
import pandas as pd
import numpy as np

pair_list = [[-1, 0, 1, 2, 3, 4],
             [0, -1, 5, 6, 7, 8],
             [1, 5, -1, 9, 10, 11],
             [2, 6, 9, -1, 12, 13],
             [3, 7, 10, 12, -1, 14],
             [4, 8, 11, 13, 14, -1]]


def channel_correct():
    correct_filename = 'result_group_channel.csv'
    correct_dataset = pd.read_csv(correct_filename)
    group_result_array = np.zeros((3 * 48 * 6, 7))
    group_result_header = "oxytype, channel, period, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    for oxy_num in range(1, 4):
        for period_num in range(1, 7):
            result_array = np.zeros((48, 7))
            for i in range(correct_dataset.shape[0]):
                oxytype = correct_dataset.iat[i, 0]
                channel = correct_dataset.iat[i, 1]
                period = correct_dataset.iat[i, 2]
                # PTSD_test_pvalue = correct_dataset.iat[i, 3]
                # HC_test_pvalue = correct_dataset.iat[i, 4]
                # t_p_value = correct_dataset.iat[i, 5]
                # mannwhitneyu_p_value = correct_dataset.iat[i, 6]
                if oxy_num == oxytype and period == period_num:
                    result_array[int(channel - 1), 0] = correct_dataset.iat[i, 0]
                    result_array[int(channel - 1), 1] = correct_dataset.iat[i, 1]
                    result_array[int(channel - 1), 2] = correct_dataset.iat[i, 2]
                    result_array[int(channel - 1), 3] = correct_dataset.iat[i, 3]
                    result_array[int(channel - 1), 4] = correct_dataset.iat[i, 4]
                    result_array[int(channel - 1), 5] = correct_dataset.iat[i, 5]
                    result_array[int(channel - 1), 6] = correct_dataset.iat[i, 6]
            raw_p_values = result_array[:, 5]
            # print(raw_p_values)

            corrected_p_values = smm.multipletests(raw_p_values, method='fdr_bh')[1]
            result_array[:, 5] = corrected_p_values
            # print(corrected_p_values)
            start = ((oxy_num - 1) * 6 + period_num - 1) * 48
            end = ((oxy_num - 1) * 6 + period_num - 1) * 48 + 48
            print(str(start) + '_' + str(end))
            group_result_array[start:end, :] = result_array[:, :]
    np.savetxt('result_group_channel.csv', group_result_array, delimiter=',',
               header=group_result_header, comments='', fmt='%.14f')


    correct_filename = 'result_task_channel.csv'
    correct_dataset = pd.read_csv(correct_filename)
    task_result_header = "oxytype, channel, period1, period2, PTSDperiod1_test_pvalue, PTSDperiod2_test_pvalue, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_test_pvalue, HCperiod2_test_pvalue, HC_p_value, HC_mannwhitneyu_p_value"
    task_result_array = np.zeros((3 * 48 * 15, 12))
    for oxy_num in range(1, 4):
        for channel_num in range(1, 49):
            result_array = np.zeros((15, 12))
            for i in range(correct_dataset.shape[0]):
                oxytype = correct_dataset.iat[i, 0]
                channel = correct_dataset.iat[i, 1]
                period1 = correct_dataset.iat[i, 2]
                period2 = correct_dataset.iat[i, 3]
                # PTSDperiod1_test_pvalue = correct_dataset.iat[i, 4]
                # PTSDperiod2_test_pvalue = correct_dataset.iat[i, 5]
                # PTSD_p_value = correct_dataset.iat[i, 6]
                # PTSD_mannwhitneyu_p_value = correct_dataset.iat[i, 7]
                # HCperiod1_test_pvalue = correct_dataset.iat[i, 8]
                # HCperiod2_test_pvalue = correct_dataset.iat[i, 9]
                # HC_p_value = correct_dataset.iat[i, 10]
                # HC_mannwhitneyu_p_value = correct_dataset.iat[i, 11]
                if oxy_num == oxytype and channel == channel_num:
                    pair_num = pair_list[int(period1)-1][int(period2)-1]
                    result_array[pair_num, 0] = correct_dataset.iat[i, 0]
                    result_array[pair_num, 1] = correct_dataset.iat[i, 1]
                    result_array[pair_num, 2] = correct_dataset.iat[i, 2]
                    result_array[pair_num, 3] = correct_dataset.iat[i, 3]
                    result_array[pair_num, 4] = correct_dataset.iat[i, 4]
                    result_array[pair_num, 5] = correct_dataset.iat[i, 5]
                    result_array[pair_num, 6] = correct_dataset.iat[i, 6]
                    result_array[pair_num, 7] = correct_dataset.iat[i, 7]
                    result_array[pair_num, 8] = correct_dataset.iat[i, 8]
                    result_array[pair_num, 9] = correct_dataset.iat[i, 9]
                    result_array[pair_num, 10] = correct_dataset.iat[i, 10]
                    result_array[pair_num, 11] = correct_dataset.iat[i, 11]
            raw_p_values = result_array[:, 6]
            corrected_p_values = smm.multipletests(raw_p_values, method='fdr_bh')[1]
            result_array[:, 6] = corrected_p_values

            raw_p_values = result_array[:, 10]
            corrected_p_values = smm.multipletests(raw_p_values, method='fdr_bh')[1]
            result_array[:, 10] = corrected_p_values

            start = ((oxy_num - 1) * 48 + channel_num - 1) * 15
            end = ((oxy_num - 1) * 48 + channel_num - 1) * 15 + 15
            print(str(start) + '_' + str(end))
            task_result_array[start:end, :] = result_array[:, :]
        np.savetxt('result_task_channel.csv', task_result_array, delimiter=',',
                   header=task_result_header, comments='', fmt='%.14f')
# for period_num in range(1, 7):
#     for another_period_num in range(period_num+1, 7):
#         print(pair_list[int(period_num-1)][int(another_period_num-1)])

channel_correct()