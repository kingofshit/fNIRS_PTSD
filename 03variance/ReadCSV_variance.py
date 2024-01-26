import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from scipy.optimize import curve_fit

PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
oxy_list = ['oxy', 'dxy', 'total']
Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']
sub_list = PTSDsub_list + HCsub_list
roi_count_array = np.array([11, 10, 10, 5, 5, 3, 2, 2])

feature_path = r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\03variance'
# data = pd.read_csv('../mean.csv', dtype=float)
data = pd.read_csv('../variance_chazhi.csv', dtype=float)

roi = pd.read_csv(r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\mni\roi.csv')
roi_name_list = roi.columns.tolist()
roi_count_list = []
for roi_num in range(0, len(roi_name_list)):
    roi_name = roi_name_list[roi_num]
    roi_channel_count = 0
    for roi_channel in roi[roi_name]:
        if not np.isnan(roi_channel):
            # print(roi_channel)
            roi_channel_count = roi_channel_count + 1
    roi_count_list.append(roi_channel_count)
roi_count_array = np.array(roi_count_list)


# # 自定义曲线函数
# def curve_func(x, a, b, c):
#     return a*np.sin(2*np.pi/12*x+b)+c


def get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label):
    # channel_num   1-48
    # period_num   1:RESTING, 2:COUNT, 3:SPEAK, 4:COUNT, 5:LISTEN, 6:COUNT
    # oxy_num   1:OXY, 2:DXY, 3:TOTAL
    # 读取 CSV 文件

    # 生成标签
    sub_num = 0
    for ALLsub_no in PTSDsub_list + HCsub_list:
        if sub_no == ALLsub_no:
            break;
        sub_num += 1
    label = 'Ch' + str(channel_num) + '_Pr' + str(period_num) + '_' + oxy_label

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return data.loc[sub_num, label]


def get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, period_num, oxy_label):
    # channel_num   1-48
    # period_num   1:RESTING, 2:COUNT, 3:SPEAK, 4:COUNT, 5:LISTEN, 6:COUNT
    # oxy_num   1:OXY, 2:DXY, 3:TOTAL
    # 读取 CSV 文件

    # 生成标签
    sub_num = 0
    for ALLsub_no in PTSDsub_list + HCsub_list:
        if sub_no == ALLsub_no:
            break;
        sub_num += 1
    label = oxy_label + '_' + roi_name + '_' + Period_name_list[period_num - 1]

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return roi_data.loc[sub_num, label]


# 分通道分析
def channel_group():
    # 分通道独立样本t检验和Mann-Whitney U 检验
    group_result_array = np.zeros((3 * 48 * 6, 7))
    group_result_header = "oxytype, channel, period, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        t_p_value_array = np.zeros((6, 48))
        mannwhitneyu_p_value_array = np.zeros((6, 48))
        for channel_num in range(1, 49):
            for period_num in range(1, 7):
                HC = []
                PTSD = []
                for sub_no in PTSDsub_list:
                    PTSD.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))
                for sub_no in HCsub_list:
                    HC.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))

                # 使用 Shapiro-Wilk 测试进行判断
                HCshapiro_test_statistic, HC_test_pvalue = stats.shapiro(HC)
                PTSDshapiro_test_statistic, PTSD_test_pvalue = stats.shapiro(PTSD)
                # 执行独立样本 t 检验
                t_statistic, t_p_value = stats.ttest_ind(HC, PTSD)
                t_p_value_array[period_num - 1, channel_num - 1] = t_p_value
                # 执行 Mann-Whitney U 检验
                mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HC, PTSD)
                mannwhitneyu_p_value_array[period_num - 1, channel_num - 1] = mannwhitneyu_p_value

                if HC_test_pvalue > 0.05 and PTSD_test_pvalue > 0.05:
                    # 使用Levene's test进行方差齐性检验
                    Levene_w, Levene_p_value = stats.levene(HC, PTSD)
                    # 如果p值＜0.05且数据符合正态分布则输出结果
                    if t_p_value < 0.05:
                        # 如果p值小于显著性水平（通常为0.05），则拒绝原假设（即认为方差不齐）
                        if Levene_p_value < 0.05:
                            print("方差不齐")
                        print('- channel ' + str(channel_num) + ' period ' + str(
                            period_num) + ' t 检验:  p value is ' + str(
                            t_p_value))
                        # plt.boxplot([np.array(HC), np.array(PTSD)])
                        # plt.xticks([1, 2], ['HC', 'PTSD'])
                        # plt.ylabel('Channel ' + str(channel_num) + '_Period ' + str(period_num) + '_' + oxy_label + '_Value')
                        # # plt.show()
                        # output_path = 'figs/mean/ttest/'
                        # if not os.path.exists(output_path):
                        #     os.makedirs(output_path)
                        # plt.savefig(output_path + 'Channel ' + str(channel_num) + '_Period ' + str(period_num) + '_' + oxy_label + '.png')
                        # plt.close()

                group_result_array[(oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 0] = oxy_num
                group_result_array[(oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 1] = channel_num
                group_result_array[(oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 2] = period_num
                group_result_array[
                    (oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 3] = PTSD_test_pvalue
                group_result_array[(oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 4] = HC_test_pvalue
                group_result_array[(oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 5] = t_p_value
                group_result_array[
                    (oxy_num - 1) * 48 * 6 + (channel_num - 1) * 6 + period_num - 1, 6] = mannwhitneyu_p_value

    np.savetxt(feature_path + '\\' + 'result_group_channel.csv', group_result_array, delimiter=',',
               header=group_result_header, comments='', fmt='%.14f')


def channel_task():
    # 分通道配对t检验和Wilcoxon符号秩检验
    result_header = "oxytype, channel, period1, period2, PTSDperiod1_test_pvalue, PTSDperiod2_test_pvalue, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_test_pvalue, HCperiod2_test_pvalue, HC_p_value, HC_mannwhitneyu_p_value"
    result_array = np.zeros((3 * 48 * 15, 12))
    channel_sum_array = np.zeros((48, 3))
    period_sum_array = np.zeros((6, 3))
    oxy_sum_array = np.zeros((3, 3))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for channel_num in range(1, 49):
            pair_no = 0
            for period_num in range(1, 7):
                for another_period_num in range(period_num, 7):
                    if period_num == another_period_num:
                        continue
                    else:
                        PTSDperiod1 = []
                        PTSDperiod2 = []
                        HCperiod1 = []
                        HCperiod2 = []
                        for sub_no in PTSDsub_list:
                            PTSDperiod1.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))
                            PTSDperiod2.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, another_period_num,
                                         oxy_label))
                        for sub_no in HCsub_list:
                            HCperiod1.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))
                            HCperiod2.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, another_period_num,
                                         oxy_label))
                        PTSDperiod1_test_statistic, PTSDperiod1_test_pvalue = stats.shapiro(PTSDperiod1)
                        PTSDperiod2_test_statistic, PTSDperiod2_test_pvalue = stats.shapiro(PTSDperiod2)
                        HCperiod1_test_statistic, HCperiod1_test_pvalue = stats.shapiro(HCperiod1)
                        HCperiod2_test_statistic, HCperiod2_test_pvalue = stats.shapiro(HCperiod2)

                        PTSD_t_statistic, PTSD_p_value = stats.ttest_rel(PTSDperiod1, PTSDperiod2)
                        PTSD_mannwhitneyu_statistic, PTSD_mannwhitneyu_p_value = stats.wilcoxon(PTSDperiod1,
                                                                                                PTSDperiod2)
                        HC_t_statistic, HC_p_value = stats.ttest_rel(HCperiod1, HCperiod2)
                        HC_mannwhitneyu_statistic, HC_mannwhitneyu_p_value = stats.wilcoxon(HCperiod1, HCperiod2)

                        if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                            if PTSD_p_value < 0.05:
                                print('- PTSD配对t检验显著： ' + oxy_label + '_' + str(channel_num) + '_' +
                                      Period_name_list[
                                          period_num - 1] + '_' + Period_name_list[another_period_num - 1] + ': ' + str(
                                    PTSD_p_value))
                        if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                            if HC_p_value < 0.05:
                                print(
                                    '- HC配对t检验显著： ' + oxy_label + '_' + str(channel_num) + '_' + Period_name_list[
                                        period_num - 1] + '_' + Period_name_list[another_period_num - 1] + ': ' + str(
                                        HC_p_value))

                        # print((oxy_num-1)*48*15+(channel_num-1)*15+pair_no)
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 0] = oxy_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 1] = channel_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 2] = period_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 3] = another_period_num
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 4] = PTSDperiod1_test_pvalue
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 5] = PTSDperiod2_test_pvalue
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 6] = PTSD_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 7] = PTSD_mannwhitneyu_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 8] = HCperiod1_test_pvalue
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 9] = HCperiod2_test_pvalue
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 10] = HC_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 11] = HC_mannwhitneyu_p_value
                        if PTSD_p_value < 0.05:
                            channel_sum_array[channel_num - 1, 0] = channel_sum_array[channel_num - 1, 0] + 1
                            period_sum_array[period_num - 1, 0] = period_sum_array[period_num - 1, 0] + 1
                            period_sum_array[another_period_num - 1, 0] = period_sum_array[
                                                                              another_period_num - 1, 0] + 1
                            oxy_sum_array[oxy_num - 1, 0] = oxy_sum_array[oxy_num - 1, 0] + 1
                            if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                                channel_sum_array[channel_num - 1, 1] = channel_sum_array[channel_num - 1, 1] + 1
                                period_sum_array[period_num - 1, 1] = period_sum_array[period_num - 1, 1] + 1
                                period_sum_array[another_period_num - 1, 1] = period_sum_array[
                                                                                  another_period_num - 1, 1] + 1
                                oxy_sum_array[oxy_num - 1, 1] = oxy_sum_array[oxy_num - 1, 1] + 1
                        if PTSD_mannwhitneyu_p_value < 0.05:
                            channel_sum_array[channel_num - 1, 2] = channel_sum_array[channel_num - 1, 2] + 1
                            period_sum_array[period_num - 1, 2] = period_sum_array[period_num - 1, 2] + 1
                            period_sum_array[another_period_num - 1, 2] = period_sum_array[
                                                                              another_period_num - 1, 2] + 1
                            oxy_sum_array[oxy_num - 1, 2] = oxy_sum_array[oxy_num - 1, 2] + 1

                        # if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                        #     if PTSD_p_value < 0.05:
                        #         print('- 配对t检验PTSD_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(another_period_num) + ': ' + str(PTSD_p_value))
                        #         plt.boxplot([np.array(PTSDperiod1), np.array(PTSDperiod2)])
                        #         plt.xticks([1, 2], [Period_name_list[period_num - 1], Period_name_list[another_period_num - 1]])
                        #         plt.ylabel('PTSD_Channel ' + str(channel_num) + '_' + oxy_label + '_Value')
                        #         # plt.show()
                        #         output_path = 'figs/mean/pairedttest/'
                        #         if not os.path.exists(output_path):
                        #             os.makedirs(output_path)
                        #         plt.savefig(output_path + 'PTSD_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(another_period_num) + oxy_label + '.png')
                        #         plt.close()
                        # else:
                        #     if PTSD_mannwhitneyu_p_value < 0.05:
                        #         print('- Wilcoxon符号秩检验PTSD_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(another_period_num) + ': ' + str(PTSD_mannwhitneyu_p_value))

                        # if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                        #     HC_t_statistic, HC_p_value = stats.ttest_rel(HCperiod1, HCperiod2)
                        #     if HC_p_value < 0.05:
                        #         print('- 配对t检验HC_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(another_period_num) + ': ' + str(HC_p_value))
                        #         plt.boxplot([np.array(HCperiod1), np.array(HCperiod2)])
                        #         plt.xticks([1, 2],[Period_name_list[period_num - 1], Period_name_list[another_period_num - 1]])
                        #         plt.ylabel('HC_Channel ' + str(channel_num) + '_' + oxy_label + '_Value')
                        #         # plt.show()
                        #         output_path = 'figs/mean/pairedttest/'
                        #         if not os.path.exists(output_path):
                        #             os.makedirs(output_path)
                        #         plt.savefig(output_path + 'HC_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(
                        #             another_period_num) + oxy_label + '.png')
                        #         plt.close()
                        # else:
                        #     HC_mannwhitneyu_statistic, HC_mannwhitneyu_p_value = stats.wilcoxon(HCperiod1, HCperiod2)
                        #     if HC_mannwhitneyu_p_value < 0.05:
                        #         print('- Wilcoxon符号秩检验HC_Ch' + str(channel_num) + '_' + str(period_num) + '_' + str(another_period_num) + ': ' + str(HC_mannwhitneyu_p_value))
                        pair_no = pair_no + 1
    np.savetxt('result_channel.csv', result_array, delimiter=',', header=result_header, comments='', fmt='%.14f')


# 分脑区分析
def roi_calculate():
    # 分脑区计算特征并存储
    roi_value_header = ""
    roi_value_array = np.zeros((len(PTSDsub_list) + len(HCsub_list), 3 * len(roi_name_list) * 6))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for roi_num in range(0, len(roi_name_list)):
            roi_name = roi_name_list[roi_num]
            for period_num in range(1, 7):
                # print('##### ' + oxy_label + '_' + roi_name + '_' + Period_name_list[period_num - 1])
                roi_value_header = roi_value_header + oxy_label + '_' + roi_name + '_' + Period_name_list[
                    period_num - 1] + ','
                # print((oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1)
                roi_channel_count = 0
                for roi_channel in roi[roi_name]:
                    if not np.isnan(roi_channel):
                        # print(roi_channel)
                        roi_channel_count = roi_channel_count + 1
                        channel_num = int(roi_channel)
                        for sub_num in range(0, len(sub_list)):
                            sub_no = sub_list[sub_num]
                            feature_value = get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num,
                                                     oxy_label)
                            roi_value_array[
                                sub_num, (oxy_num - 1) * len(
                                    roi_name_list) * 6 + roi_num * 6 + period_num - 1] += feature_value
                            # roi_value_array[(oxy_num-1)*8*6+(np.sum(roi_count_array[:roi_num])+roi_channel_count)*6+period_num-1, ]
            for period_num in range(1, 7):
                for sub_num in range(0, len(sub_list)):
                    roi_value_array[sub_num, (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1] = (
                            roi_value_array[
                                sub_num, (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1] /
                            roi_count_array[roi_num])
                # print('roi_channel_count:  '+ str(roi_channel_count))
    roi_value_header = roi_value_header[:-1]
    np.savetxt(feature_path + '\\' + 'value_roi.csv', roi_value_array, delimiter=',', header=roi_value_header,
               comments='',
               fmt='%.14f')


def roi_group():
    # 分脑区配对t检验和Wilcoxon符号秩检验
    roi_result_header = "oxytype, roi, period1, period2, PTSDperiod1_test_pvalue, PTSDperiod2_test_pvalue, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_test_pvalue, HCperiod2_test_pvalue, HC_p_value, HC_mannwhitneyu_p_value"
    roi_data = pd.read_csv(feature_path + '\\' + 'value_roi.csv', dtype=float)
    roi_result_array = np.zeros((3 * len(roi_name_list) * 15, 12))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for roi_num in range(0, len(roi_name_list)):
            roi_name = roi_name_list[roi_num]
            pair_no = 0
            for period_num in range(1, 7):
                for another_period_num in range(period_num, 7):
                    if period_num == another_period_num:
                        continue
                    else:
                        PTSDperiod1 = []
                        PTSDperiod2 = []
                        HCperiod1 = []
                        HCperiod2 = []
                        for sub_no in PTSDsub_list:
                            PTSDperiod1.append(
                                get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, period_num,
                                             oxy_label))
                            PTSDperiod2.append(
                                get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, another_period_num,
                                             oxy_label))
                        for sub_no in HCsub_list:
                            HCperiod1.append(
                                get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, period_num,
                                             oxy_label))
                            HCperiod2.append(
                                get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, another_period_num,
                                             oxy_label))

                        # 检验正态性
                        PTSDperiod1_test_statistic, PTSDperiod1_test_pvalue = stats.shapiro(PTSDperiod1)
                        PTSDperiod2_test_statistic, PTSDperiod2_test_pvalue = stats.shapiro(PTSDperiod2)
                        HCperiod1_test_statistic, HCperiod1_test_pvalue = stats.shapiro(HCperiod1)
                        HCperiod2_test_statistic, HCperiod2_test_pvalue = stats.shapiro(HCperiod2)

                        # 配对t检验和Wilcoxon符号秩检验
                        PTSD_t_statistic, PTSD_p_value = stats.ttest_rel(PTSDperiod1, PTSDperiod2)
                        PTSD_mannwhitneyu_statistic, PTSD_mannwhitneyu_p_value = stats.wilcoxon(PTSDperiod1,
                                                                                                PTSDperiod2)
                        HC_t_statistic, HC_p_value = stats.ttest_rel(HCperiod1, HCperiod2)
                        HC_mannwhitneyu_statistic, HC_mannwhitneyu_p_value = stats.wilcoxon(HCperiod1, HCperiod2)

                        if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                            if PTSD_p_value < 0.05:
                                print('- PTSD配对t检验显著： ' + oxy_label + '_' + roi_name + '_' + Period_name_list[
                                    period_num - 1] + '_' + Period_name_list[another_period_num - 1] + ': ' + str(
                                    PTSD_p_value))
                        if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                            if HC_p_value < 0.05:
                                print('- HC配对t检验显著： ' + oxy_label + '_' + roi_name + '_' + Period_name_list[
                                    period_num - 1] + '_' + Period_name_list[another_period_num - 1] + ': ' + str(
                                    HC_p_value))

                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 0] = oxy_num
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 1] = roi_num
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 2] = period_num
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 3] = another_period_num
                        roi_result_array[(oxy_num - 1) * len(
                            roi_name_list) * 15 + roi_num * 15 + pair_no, 4] = PTSDperiod1_test_pvalue
                        roi_result_array[(oxy_num - 1) * len(
                            roi_name_list) * 15 + roi_num * 15 + pair_no, 5] = PTSDperiod2_test_pvalue
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 6] = PTSD_p_value
                        roi_result_array[(oxy_num - 1) * len(
                            roi_name_list) * 15 + roi_num * 15 + pair_no, 7] = PTSD_mannwhitneyu_p_value
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 8] = HCperiod1_test_pvalue
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 9] = HCperiod2_test_pvalue
                        roi_result_array[
                            (oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 10] = HC_p_value
                        roi_result_array[(oxy_num - 1) * len(
                            roi_name_list) * 15 + roi_num * 15 + pair_no, 11] = HC_mannwhitneyu_p_value
                        pair_no = pair_no + 1
    np.savetxt(feature_path + '\\' + 'result_roi.csv', roi_result_array, delimiter=',', header=roi_result_header,
               comments='', fmt='%.14f')


def roi_task():
    # 分脑区独立样本t检验和Mann-Whitney U 检验
    roi_data = pd.read_csv(feature_path + '\\' + 'value_roi.csv', dtype=float)
    roi_group_result_header = "oxytype, roi, period, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    roi_group_result_array = np.zeros((3 * len(roi_name_list) * 6, 7))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for roi_num in range(0, len(roi_name_list)):
            roi_name = roi_name_list[roi_num]
            for period_num in range(1, 7):
                PTSD_list = []
                HC_list = []
                for sub_no in PTSDsub_list:
                    PTSD_list.append(
                        get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, period_num, oxy_label))
                for sub_no in HCsub_list:
                    HC_list.append(
                        get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, period_num, oxy_label))

                # 检验正态性
                PTSD_test_statistic, PTSD_test_pvalue = stats.shapiro(PTSD_list)
                HC_test_statistic, HC_test_pvalue = stats.shapiro(HC_list)
                # 执行独立样本 t 检验
                t_statistic, t_p_value = stats.ttest_ind(HC_list, PTSD_list)
                # 执行 Mann-Whitney U 检验
                mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HC_list, PTSD_list)

                if PTSD_test_pvalue > 0.05 and HC_test_pvalue > 0.05:
                    if t_p_value < 0.05:
                        print('- 独立样本t检验显著： ' + oxy_label + '_' + roi_name + '_' + Period_name_list[
                            period_num - 1] + ': ' + str(t_p_value))
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 0] = oxy_num
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 1] = roi_num
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 2] = period_num
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 3] = PTSD_test_pvalue
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 4] = HC_test_pvalue
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 5] = t_p_value
                roi_group_result_array[
                    (oxy_num - 1) * len(roi_name_list) * 6 + roi_num * 6 + period_num - 1, 6] = mannwhitneyu_p_value
    np.savetxt(feature_path + '\\' + 'result_group_roi.csv', roi_group_result_array, delimiter=',',
               header=roi_group_result_header, comments='', fmt='%.14f')


channel_group()
channel_task()
roi_calculate()
roi_group()
roi_task()
# # 按照通道画图
# # 选择血氧数据 1:OXY, 2:DXY, 3:TOTAL
# oxy_num = 2;
# oxy_label = oxy_list[oxy_num - 1]
# for channel_num in range(1, 49):
#     # 创建图形和轴对象
#     fig, ax = plt.subplots()
#     draw_X = [1, 2, 3, 4, 5, 6]
#     for sub_no in PTSDsub_list:
#         draw_Y = []
#         for period_num in range(1, 7):
#             draw_Y.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))
#
#         # popt, _ = curve_fit(curve_func, draw_X, draw_Y)
#         # # 生成拟合曲线的数据
#         # x_fit = np.linspace(1, 6, 100)
#         # y_fit = curve_func(x_fit, *popt)
#         # 绘制散点图和拟合曲线
#         plt.scatter(draw_X, draw_Y, color='orange')
#         plt.plot(draw_X, draw_Y, label=sub_no, color='orange')
#         # plt.plot(x_fit, y_fit, label=sub_no, color='orange')
#
#     for sub_no in HCsub_list:
#         draw_Y = []
#         for period_num in range(1, 7):
#             draw_Y.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, period_num, oxy_label))
#
#         # popt, _ = curve_fit(curve_func, draw_X, draw_Y)
#         # # 生成拟合曲线的数据
#         # x_fit = np.linspace(1, 6, 100)
#         # y_fit = curve_func(x_fit, *popt)
#         # 绘制散点图和拟合曲线
#         plt.scatter(draw_X, draw_Y, color='skyblue')
#         plt.plot(draw_X, draw_Y, label=sub_no, color='skyblue')
#         # plt.plot(x_fit, y_fit, label=sub_no, color='skyblue')
#
#     # 输出图形
#     output_path = r'D:/fNIRS_Data/zishu/figs/mean_chazhi/'
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#     plt.savefig(output_path + str(channel_num) + '.png')
