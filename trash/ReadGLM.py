# Import numpy and scipy
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import os

xlsx_name = "D:\\fNIRS_Data\\zishu\\NIRS_KIT_Individual_Analysis\\" + "result.xlsx"
Features = ["Dxy\\", "Oxy\\", "Total\\"]
# Features = ["Dxy\\"]
Betas = ["beta_0\\", "beta_1\\", "beta_2\\", "beta_3\\", "beta_4\\", "beta_5\\", "beta_6\\"]
# Betas = ["beta_0\\"]
Channels = ['value_Channel1', 'value_Channel2', 'value_Channel3', 'value_Channel4'
, 'value_Channel5', 'value_Channel6', 'value_Channel7', 'value_Channel8', 'value_Channel9', 'value_Channel10'
, 'value_Channel11', 'value_Channel12', 'value_Channel13', 'value_Channel14', 'value_Channel15', 'value_Channel16'
, 'value_Channel17', 'value_Channel18', 'value_Channel19', 'value_Channel20', 'value_Channel21', 'value_Channel22'
, 'value_Channel23', 'value_Channel24', 'value_Channel25', 'value_Channel26', 'value_Channel27', 'value_Channel28'
, 'value_Channel29', 'value_Channel30', 'value_Channel31', 'value_Channel32', 'value_Channel33', 'value_Channel34'
, 'value_Channel35', 'value_Channel36', 'value_Channel37', 'value_Channel38', 'value_Channel39', 'value_Channel40'
, 'value_Channel41', 'value_Channel42', 'value_Channel43', 'value_Channel44', 'value_Channel45', 'value_Channel46'
, 'value_Channel47', 'value_Channel48']
# Channels = ['value_Channel1']
show = 0
save = 1

data = pd.read_excel(io=xlsx_name)
for feature in Features:
    for beta in Betas:
        Feature = feature + beta
        for channel in Channels:
            HCdata = []
            PTSDdata = []
            for i in range(data.shape[0]):
                if Feature == data.loc[i, "Feature"]:
                    if data.loc[i, "Group"] == "HC\\":
                        HCdata.append(data.loc[i, channel])
                    elif data.loc[i, "Group"] == "PTSD\\":
                        PTSDdata.append(data.loc[i, channel])
            # Run a two sample t-test to compare the two samples
            # 使用 Shapiro-Wilk 测试进行判断
            HCshapiro_test_statistic, HCshapiro_test_pvalue = stats.shapiro(HCdata)
            PTSDshapiro_test_statistic, PTSDshapiro_test_pvalue = stats.shapiro(PTSDdata)
            if HCshapiro_test_pvalue > 0.05 and PTSDshapiro_test_pvalue > 0.05:
                # 使用Levene's test进行方差齐性检验
                Levene_w, Levene_p_value = stats.levene(HCdata, PTSDdata)
                tstat, pval = stats.ttest_ind(a=np.array(HCdata), b=np.array(PTSDdata), alternative="two-sided")
                if pval < 0.05:
                    # 如果p值小于显著性水平（通常为0.05），则拒绝原假设（即认为方差不齐）
                    if Levene_p_value < 0.05:
                        print("方差不齐")
                    print("- " + Feature + channel + ' pvalue is: ' + str(pval))
                    plt.boxplot([np.array(HCdata), np.array(PTSDdata)])
                    plt.xticks([1, 2], ['HC', 'PTSD'])
                    plt.ylabel(Feature + channel)
                    # plt.show()
                    output_path = 'figs/GLM/ttest/'
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    filename = ''
                    filename = filename + Feature + channel
                    filename = filename.replace('\\', '_')
                    plt.savefig(output_path + filename + '.png')
                    plt.close()
            # else:
            #     # 执行 Mann-Whitney U 检验
            #     mannwhitneyu_statistic, mannwhitneyu_p_value = stats.mannwhitneyu(HCdata, PTSDdata)
            #     # 如果p值＜0.05则输出结果
            #     if mannwhitneyu_p_value < 0.05:
            #         print("- " + Feature + channel + ' mannwhitneyu_pvalue is: ' + str(mannwhitneyu_p_value))