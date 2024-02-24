import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from scipy.optimize import curve_fit

periodlist = ["1RESTING", "3SPEAK", "5LISTEN"]
Groups = ["HC\\", 'PTSD\\']
Network_single_featrue_list = ['Assortativity\\ar.txt', 'Hierarchy\\ab.txt', 'NetworkEfficiency\\aEg.txt',
                               'NetworkEfficiency\\aEloc.txt', 'SmallWorld\\aCp.txt', 'SmallWorld\\aGamma.txt',
                               'SmallWorld\\aLambda.txt', 'SmallWorld\\aLp.txt', 'SmallWorld\\aSigma.txt',
                               'Synchronization\\as.txt']
Network_multiple_featrue_list = ['RichClub\\phi_real_Thres001.txt']

PTSDsub_list = pd.read_csv('..\\PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('..\\HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list


def get_feature(data, PTSDsub_list, HCsub_list, sub_no, period_num):
    sub_num = 0
    for ALLsub_no in PTSDsub_list + HCsub_list:
        if sub_no == ALLsub_no:
            break;
        sub_num += 1
    label = periodlist[period_num]
    return data.loc[sub_num, label]



# 分通道分析
def group():
    group_result_array = np.zeros((len(Network_single_featrue_list)*len(periodlist),6))
    group_result_header = "feature, period, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    for Network_single_featrue_num in range(0, len(Network_single_featrue_list)):
        csv_name = Network_single_featrue_list[Network_single_featrue_num].replace('\\', '_').replace('.txt', '.csv')
        data = pd.read_csv(csv_name, dtype=float)
        for period_num in range(0, len(periodlist)):
            HC = []
            PTSD = []
            for sub_no in PTSDsub_list:
                PTSD.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, period_num))
            for sub_no in HCsub_list:
                HC.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, period_num))
            # 使用 Shapiro-Wilk 测试进行判断
            HCshapiro_test_statistic, HC_test_pvalue = stats.shapiro(HC)
            PTSDshapiro_test_statistic, PTSD_test_pvalue = stats.shapiro(PTSD)
            # 执行独立样本 t 检验
            t_statistic, t_p_value = stats.ttest_ind(HC, PTSD)
            # 执行 Mann-Whitney U 检验
            mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HC, PTSD)

            row_num = Network_single_featrue_num*len(periodlist)+period_num
            group_result_array[row_num, 0] = Network_single_featrue_num
            group_result_array[row_num, 1] = period_num
            group_result_array[row_num, 2] = PTSD_test_pvalue
            group_result_array[row_num, 3] = HC_test_pvalue
            group_result_array[row_num, 4] = t_p_value
            group_result_array[row_num, 5] = mannwhitneyu_p_value

    np.savetxt('result_group_channel.csv', group_result_array, delimiter=',',
               header=group_result_header, comments='', fmt='%.14f')


def task():
    # 分通道配对t检验和Wilcoxon符号秩检验
    result_header = "feature, period1, period2, PTSDperiod1_test_pvalue, PTSDperiod2_test_pvalue, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_test_pvalue, HCperiod2_test_pvalue, HC_p_value, HC_mannwhitneyu_p_value"
    result_array = np.zeros((len(Network_single_featrue_list)*3, 11))
    for Network_single_featrue_num in range(0, len(Network_single_featrue_list)):
        csv_name = Network_single_featrue_list[Network_single_featrue_num].replace('\\', '_').replace('.txt', '.csv')
        data = pd.read_csv(csv_name, dtype=float)
        pair_num = 0
        for period_num in range(0, len(periodlist)):
            for another_period_num in range(period_num+1, len(periodlist)):

                PTSDperiod1 = []
                PTSDperiod2 = []
                HCperiod1 = []
                HCperiod2 = []
                for sub_no in PTSDsub_list:
                    PTSDperiod1.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, period_num))
                    PTSDperiod2.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, another_period_num))
                for sub_no in HCsub_list:
                    HCperiod1.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, period_num))
                    HCperiod2.append(get_feature(data, PTSDsub_list, HCsub_list, sub_no, another_period_num))
                PTSDperiod1_test_statistic, PTSDperiod1_test_pvalue = stats.shapiro(PTSDperiod1)
                PTSDperiod2_test_statistic, PTSDperiod2_test_pvalue = stats.shapiro(PTSDperiod2)
                HCperiod1_test_statistic, HCperiod1_test_pvalue = stats.shapiro(HCperiod1)
                HCperiod2_test_statistic, HCperiod2_test_pvalue = stats.shapiro(HCperiod2)

                PTSD_t_statistic, PTSD_p_value = stats.ttest_rel(PTSDperiod1, PTSDperiod2)
                PTSD_mannwhitneyu_statistic, PTSD_mannwhitneyu_p_value = stats.wilcoxon(PTSDperiod1,
                                                                                        PTSDperiod2)
                HC_t_statistic, HC_p_value = stats.ttest_rel(HCperiod1, HCperiod2)
                HC_mannwhitneyu_statistic, HC_mannwhitneyu_p_value = stats.wilcoxon(HCperiod1, HCperiod2)

                row_num = Network_single_featrue_num*3 + pair_num
                result_array[row_num, 0] = Network_single_featrue_num
                result_array[row_num, 1] = period_num
                result_array[row_num, 2] = another_period_num
                result_array[row_num, 3] = PTSDperiod1_test_pvalue
                result_array[row_num, 4] = PTSDperiod2_test_pvalue
                result_array[row_num, 5] = PTSD_p_value
                result_array[row_num, 6] = PTSD_mannwhitneyu_p_value
                result_array[row_num, 7] = HCperiod1_test_pvalue
                result_array[row_num, 8] = HCperiod2_test_pvalue
                result_array[row_num, 9] = HC_p_value
                result_array[row_num, 10] = HC_mannwhitneyu_p_value

                pair_num += 1
    np.savetxt('result_task_channel.csv', result_array, delimiter=',', header=result_header, comments='', fmt='%.14f')


group()
task()