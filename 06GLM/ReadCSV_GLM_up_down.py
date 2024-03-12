import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from scipy.optimize import curve_fit

feature_path = r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\06GLM'
# data = pd.read_csv('../mean.csv', dtype=float)
data = pd.read_csv('../GLM_chazhi.csv', dtype=float)
roi_percent = pd.read_csv(r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\mni\roi_percent.csv')

PTSDsub_list = pd.read_csv('../PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('../HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
sub_list = PTSDsub_list + HCsub_list

oxy_list = ['oxy', 'dxy', 'total']
Period_name_list = ['Resting', 'Count1', 'Speak', 'Count2', 'Listen', 'Count3']
Beta_list = ["beta0", "beta1", "beta2", "beta3", "beta4", "beta5", "beta6"]

roi_name_list = []
for item_num in range(roi_percent.shape[0]):
    item_in_list = 0
    this_roi_name = str(roi_percent.loc[item_num, 'roi_num'])
    for roi_name in roi_name_list:
        if this_roi_name == roi_name:
            item_in_list = 1
            break
    if item_in_list == 0:
        roi_name_list.append(this_roi_name)




def get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label):
    # channel_num   1-48
    # beta_num   0-6
    # oxy_num   1:OXY, 2:DXY, 3:TOTAL
    # 读取 CSV 文件

    # 生成标签
    sub_num = 0
    for ALLsub_no in PTSDsub_list + HCsub_list:
        if sub_no == ALLsub_no:
            break;
        sub_num += 1
    label = oxy_label + "_beta" + str(beta_num) + '_Ch' + str(channel_num)

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return data.loc[sub_num, label]


def get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, beta_num, oxy_label):
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
    label = oxy_label + '_' + roi_name + '_' + Beta_list[beta_num]

    # # 打印标签和数据
    # print(sub_no + '  ' + label + ': ' + str(data.loc[sub_num, label]))
    return roi_data.loc[sub_num, label]


# 分通道分析
def channel_group():
    # 分通道独立样本t检验和Mann-Whitney U 检验
    print('------分通道组间------')
    group_result_array = np.zeros((3 * 48 * 7, 7))
    group_result_header = "oxytype, channel, beta, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        t_p_value_array = np.zeros((7, 48))
        mannwhitneyu_p_value_array = np.zeros((7, 48))
        for channel_num in range(1, 49):
            for beta_num in range(0, 7):
                HC = []
                PTSD = []
                for sub_no in PTSDsub_list:
                    PTSD.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label))
                for sub_no in HCsub_list:
                    HC.append(get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label))

                # 使用 Shapiro-Wilk 测试进行判断
                HCshapiro_test_statistic, HC_test_pvalue = stats.shapiro(HC)
                PTSDshapiro_test_statistic, PTSD_test_pvalue = stats.shapiro(PTSD)
                # 执行独立样本 t 检验
                t_statistic, t_p_value = stats.ttest_ind(HC, PTSD)
                t_p_value_array[beta_num, channel_num - 1] = t_p_value
                # 执行 Mann-Whitney U 检验
                mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HC, PTSD)
                mannwhitneyu_p_value_array[beta_num, channel_num - 1] = mannwhitneyu_p_value

                if HC_test_pvalue > 0.05 and PTSD_test_pvalue > 0.05:
                    # 使用Levene's test进行方差齐性检验
                    Levene_w, Levene_p_value = stats.levene(HC, PTSD)
                    # 如果p值＜0.05且数据符合正态分布则输出结果
                    if t_p_value < 0.05:
                        # 如果p值小于显著性水平（通常为0.05），则拒绝原假设（即认为方差不齐）
                        if Levene_p_value < 0.05:
                            print("方差不齐")
                        print('- channel ' + str(channel_num) + ' beta ' + str(
                            beta_num) + ' t 检验:  p value is ' + str(
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

                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 0] = oxy_num
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 1] = channel_num
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 2] = beta_num
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 3] = PTSD_test_pvalue
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 4] = HC_test_pvalue
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 5] = t_p_value
                group_result_array[(oxy_num - 1) * 48 * 7 + (channel_num - 1) * 7 + beta_num , 6] = mannwhitneyu_p_value

    np.savetxt(feature_path + '\\' + 'result_group_channel.csv', group_result_array, delimiter=',',
               header=group_result_header, comments='', fmt='%.14f')


def channel_task():
    # 分通道配对t检验和Wilcoxon符号秩检验
    print('------分通道任务间------')
    result_header = "oxytype, channel, beta1, beta2, PTSDperiod1_mean, PTSDperiod2-1_mean, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_mean, HCperiod2-1_mean, HC_p_value, HC_mannwhitneyu_p_value"
    result_array = np.zeros((3 * 48 * 21, 12))
    channel_sum_array = np.zeros((48, 3))
    beta_sum_array = np.zeros((7, 3))
    oxy_sum_array = np.zeros((3, 3))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for channel_num in range(1, 49):
            pair_no = 0
            for beta_num in range(0, 7):
                for another_beta_num in range(beta_num+1, 7):
                    if beta_num == another_beta_num:
                        continue
                    else:
                        PTSDperiod1 = []
                        PTSDperiod2 = []
                        HCperiod1 = []
                        HCperiod2 = []
                        for sub_no in PTSDsub_list:
                            PTSDperiod1.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label))
                            PTSDperiod2.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, another_beta_num, oxy_label))
                        for sub_no in HCsub_list:
                            HCperiod1.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label))
                            HCperiod2.append(
                                get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, another_beta_num, oxy_label))
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
                                      Beta_list[beta_num] + '_' + Beta_list[another_beta_num] + ': ' + str(
                                    PTSD_p_value))
                        if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                            if HC_p_value < 0.05:
                                print('- HC配对t检验显著： ' + oxy_label + '_' + str(channel_num) + '_' +
                                      Beta_list[beta_num] + '_' + Beta_list[another_beta_num] + ': ' + str(
                                    HC_p_value))
                        ptsd_sub_task_1 = sum(PTSDperiod1) / len(PTSDperiod1)
                        ptsd_sub_task_2 = sum(PTSDperiod2) / len(PTSDperiod2)-sum(PTSDperiod1) / len(PTSDperiod1)
                        hc_sub_task_1 = sum(HCperiod1) / len(HCperiod1)
                        hc_sub_task_2 = sum(HCperiod2) / len(HCperiod2)-sum(HCperiod1) / len(HCperiod1)
                        # print((oxy_num-1)*48*15+(channel_num-1)*15+pair_no)
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 0] = oxy_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 1] = channel_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 2] = beta_num
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 3] = another_beta_num
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 4] = ptsd_sub_task_1
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 5] = ptsd_sub_task_2
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 6] = PTSD_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 7] = PTSD_mannwhitneyu_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 8] = hc_sub_task_1
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 9] = hc_sub_task_2
                        result_array[(oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 10] = HC_p_value
                        result_array[
                            (oxy_num - 1) * 48 * 15 + (channel_num - 1) * 15 + pair_no, 11] = HC_mannwhitneyu_p_value
                        if PTSD_p_value < 0.05:
                            channel_sum_array[channel_num - 1, 0] = channel_sum_array[channel_num - 1, 0] + 1
                            beta_sum_array[beta_num, 0] = beta_sum_array[beta_num, 0] + 1
                            beta_sum_array[another_beta_num, 0] = beta_sum_array[another_beta_num, 0] + 1
                            oxy_sum_array[oxy_num - 1, 0] = oxy_sum_array[oxy_num - 1, 0] + 1
                            if PTSDperiod1_test_pvalue > 0.05 and PTSDperiod2_test_pvalue > 0.05:
                                channel_sum_array[channel_num - 1, 1] = channel_sum_array[channel_num - 1, 1] + 1
                                beta_sum_array[beta_num, 1] = beta_sum_array[beta_num, 1] + 1
                                beta_sum_array[another_beta_num, 1] = beta_sum_array[another_beta_num, 1] + 1
                                oxy_sum_array[oxy_num - 1, 1] = oxy_sum_array[oxy_num - 1, 1] + 1
                        if PTSD_mannwhitneyu_p_value < 0.05:
                            channel_sum_array[channel_num - 1, 2] = channel_sum_array[channel_num - 1, 2] + 1
                            beta_sum_array[beta_num, 2] = beta_sum_array[beta_num, 2] + 1
                            beta_sum_array[another_beta_num, 2] = beta_sum_array[another_beta_num, 2] + 1
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
    np.savetxt('result_task_up_down.csv', result_array, delimiter=',', header=result_header, comments='', fmt='%.14f')


# 分脑区分析
def roi_calculate():
    # 分脑区计算特征并存储
    print('------分脑区计算------')
    roi_value_header = ""
    roi_value_array = np.zeros((len(PTSDsub_list) + len(HCsub_list), 3 * len(roi_name_list) * 7))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        for roi_num in range(0, len(roi_name_list)):
            for item_num in range(roi_percent.shape[0]):
                if str(roi_percent.loc[item_num, 'roi_num']) == roi_name_list[roi_num]:
                    channel_num = roi_percent.loc[item_num, 'channel_num']
                    for sub_num in range(0, len(sub_list)):
                        sub_no = sub_list[sub_num]
                        for beta_num in range(0, 7):
                            feature_value = get_mean(data, PTSDsub_list, HCsub_list, sub_no, channel_num, beta_num, oxy_label)
                            feature_value = feature_value*roi_percent.loc[item_num, 'channel_percentage']
                            roi_value_array[sub_num, (oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 7 + beta_num] += feature_value
                            # print(str(sub_num)+'_'+str((oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 7 + beta_num))
                            # print(roi_value_array[sub_num, (oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 7 + beta_num])

            for beta_num in range(0, 7):
                roi_value_header = roi_value_header + oxy_label + '_' + roi_name_list[roi_num] + '_' + Beta_list[beta_num] + ','


    roi_value_header = roi_value_header[:-1]
    np.savetxt(feature_path + '\\' + 'value_roi.csv', roi_value_array, delimiter=',', header=roi_value_header,
               comments='',
               fmt='%.14f')


def roi_task():
    # 分脑区配对t检验和Wilcoxon符号秩检验
    print('------分脑区任务间------')
    roi_result_header = "oxytype, roi, beta1, beta2, PTSDperiod1_test_pvalue, PTSDperiod2_test_pvalue, PTSD_p_value, PTSD_mannwhitneyu_p_value, HCperiod1_test_pvalue, HCperiod2_test_pvalue, HC_p_value, HC_mannwhitneyu_p_value"
    roi_data = pd.read_csv(feature_path + '\\' + 'value_roi.csv', dtype=float)
    roi_result_array = np.zeros((3 * len(roi_name_list) * 21, 12))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for roi_num in range(0, len(roi_name_list)):
            roi_name = roi_name_list[roi_num]
            pair_no = 0
            for beta_num in range(0, 7):
                for another_beta_num in range(beta_num, 7):
                    if beta_num == another_beta_num:
                        continue
                    else:
                        PTSDperiod1 = []
                        PTSDperiod2 = []
                        HCperiod1 = []
                        HCperiod2 = []
                        for sub_no in PTSDsub_list:
                            PTSDperiod1.append(get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, beta_num, oxy_label))
                            PTSDperiod2.append(get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, another_beta_num, oxy_label))
                        for sub_no in HCsub_list:
                            HCperiod1.append(get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, beta_num, oxy_label))
                            HCperiod2.append(get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, another_beta_num, oxy_label))

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
                                print('- PTSD配对t检验显著： ' + oxy_label + '_' + roi_name + '_' + Beta_list[beta_num] + '_' + Beta_list[another_beta_num] + ': ' + str(
                                    PTSD_p_value))
                        if HCperiod1_test_pvalue > 0.05 and HCperiod2_test_pvalue > 0.05:
                            if HC_p_value < 0.05:
                                print('- HC配对t检验显著： ' + oxy_label + '_' + roi_name + '_' + Beta_list[beta_num] + '_' + Beta_list[another_beta_num] + ': ' + str(
                                    HC_p_value))

                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 0] = oxy_num
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 1] = roi_num
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 2] = beta_num
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 3] = another_beta_num
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 4] = PTSDperiod1_test_pvalue
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 5] = PTSDperiod2_test_pvalue
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 6] = PTSD_p_value
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 7] = PTSD_mannwhitneyu_p_value
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 8] = HCperiod1_test_pvalue
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 9] = HCperiod2_test_pvalue
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 10] = HC_p_value
                        roi_result_array[(oxy_num - 1) * len(roi_name_list) * 15 + roi_num * 15 + pair_no, 11] = HC_mannwhitneyu_p_value
                        pair_no = pair_no + 1
    np.savetxt(feature_path + '\\' + 'result_task_roi.csv', roi_result_array, delimiter=',', header=roi_result_header,
               comments='', fmt='%.14f')


def roi_group():
    # 分脑区独立样本t检验和Mann-Whitney U 检验
    print('------分脑区组间------')
    roi_data = pd.read_csv(feature_path + '\\' + 'value_roi.csv', dtype=float)
    roi_group_result_header = "oxytype, roi, beta, PTSD_test_pvalue, HC_test_pvalue, t_p_value, mannwhitneyu_p_value"
    roi_group_result_array = np.zeros((3 * len(roi_name_list) * 7, 7))
    for oxy_num in range(1, 4):
        oxy_label = oxy_list[oxy_num - 1]
        # print('##### ' + oxy_label)
        for roi_num in range(0, len(roi_name_list)):
            roi_name = roi_name_list[roi_num]
            for beta_num in range(0, 7):
                PTSD_list = []
                HC_list = []
                for sub_no in PTSDsub_list:
                    PTSD_list.append(
                        get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, beta_num, oxy_label))
                for sub_no in HCsub_list:
                    HC_list.append(
                        get_roi_data(roi_data, PTSDsub_list, HCsub_list, sub_no, roi_name, beta_num, oxy_label))

                # print(oxy_label + '_' + roi_name + '_' + Beta_list[beta_num])
                # print(PTSD_list)
                # print(HC_list)
                # 检验正态性
                PTSD_test_statistic, PTSD_test_pvalue = stats.shapiro(PTSD_list)
                HC_test_statistic, HC_test_pvalue = stats.shapiro(HC_list)
                # 执行独立样本 t 检验
                t_statistic, t_p_value = stats.ttest_ind(HC_list, PTSD_list)
                # 执行 Mann-Whitney U 检验
                mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HC_list, PTSD_list)

                if PTSD_test_pvalue > 0.05 and HC_test_pvalue > 0.05:
                    if t_p_value < 0.05:
                        print('- 独立样本t检验显著： ' + oxy_label + '_' + roi_name + '_' + Beta_list[beta_num] + ': ' + str(t_p_value))
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 0] = oxy_num
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 1] = roi_num
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 2] = beta_num
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 3] = PTSD_test_pvalue
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 4] = HC_test_pvalue
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 5] = t_p_value
                roi_group_result_array[(oxy_num - 1) * len(roi_name_list) * 7 + roi_num * 6 + beta_num, 6] = mannwhitneyu_p_value
    np.savetxt(feature_path + '\\' + 'result_group_roi.csv', roi_group_result_array, delimiter=',',
               header=roi_group_result_header, comments='', fmt='%.14f')


# channel_group()
channel_task()
# roi_calculate()
# roi_group()
# roi_task()


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
