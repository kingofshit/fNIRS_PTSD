import scipy.io
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis

Rawdatapaths = ["D:\\fNIRS_Data\\zishu\\NIRS_KIT_1RESTING\\",
                "D:\\fNIRS_Data\\zishu\\NIRS_KIT_2COUNT\\",
                "D:\\fNIRS_Data\\zishu\\NIRS_KIT_3SPEAK\\",
                "D:\\fNIRS_Data\\zishu\\NIRS_KIT_4COUNT\\",
                "D:\\fNIRS_Data\\zishu\\NIRS_KIT_5LISTEN\\",
                "D:\\fNIRS_Data\\zishu\\NIRS_KIT_6COUNT\\"]
Groups = ["HC\\", 'PTSD\\']
PTSDsub_list = pd.read_csv('PTSDsub_list.csv', dtype=str)
PTSDsub_list = PTSDsub_list.values.tolist()[0]
HCsub_list = pd.read_csv('HCsub_list.csv', dtype=str)
HCsub_list = HCsub_list.values.tolist()[0]
Subjects = PTSDsub_list + HCsub_list
LenMin = [3299, 333, 1365, 334, 1320, 333]


def feature_len(fnirs_oxyData, fnirs_dxyData, fnirs_totalData):
    oxy_feature = fnirs_oxyData.shape[0]
    dxy_feature = fnirs_dxyData.shape[0]
    total_feature = fnirs_totalData.shape[0]
    return oxy_feature, dxy_feature, total_feature


def feature_mean(fnirs_oxyData, fnirs_dxyData, fnirs_totalData, channel_num):
    oxy_feature = np.mean(fnirs_oxyData[:, channel_num])
    dxy_feature = np.mean(fnirs_dxyData[:, channel_num])
    total_feature = np.mean(fnirs_totalData[:, channel_num])
    return oxy_feature, dxy_feature, total_feature


def feature_integral(fnirs_oxyData, fnirs_dxyData, fnirs_totalData, channel_num, period_no):
    # print(LenMin[period_no])
    oxy_feature = np.sum(fnirs_oxyData[:LenMin[period_no], channel_num])
    dxy_feature = np.sum(fnirs_dxyData[:LenMin[period_no], channel_num])
    total_feature = np.sum(fnirs_totalData[:LenMin[period_no], channel_num])
    return oxy_feature, dxy_feature, total_feature


def feature_variance(fnirs_oxyData, fnirs_dxyData, fnirs_totalData, channel_num):
    oxy_feature = np.sqrt(np.var(fnirs_oxyData[:, channel_num], ddof=1))
    dxy_feature = np.sqrt(np.var(fnirs_dxyData[:, channel_num], ddof=1))
    total_feature = np.sqrt(np.var(fnirs_totalData[:, channel_num], ddof=1))
    return oxy_feature, dxy_feature, total_feature


def feature_skewness(fnirs_oxyData, fnirs_dxyData, fnirs_totalData, channel_num):
    oxy_feature = skew(fnirs_oxyData[:, channel_num])
    dxy_feature = skew(fnirs_dxyData[:, channel_num])
    total_feature = skew(fnirs_totalData[:, channel_num])
    return oxy_feature, dxy_feature, total_feature


def feature_kurtosis(fnirs_oxyData, fnirs_dxyData, fnirs_totalData, channel_num):
    oxy_feature = kurtosis(fnirs_oxyData[:, channel_num])
    dxy_feature = kurtosis(fnirs_dxyData[:, channel_num])
    total_feature = kurtosis(fnirs_totalData[:, channel_num])
    return oxy_feature, dxy_feature, total_feature


len_array = np.zeros((len(Subjects), 6))
mean_array = np.zeros((len(Subjects), 6 * 48 * 3))
integral_array = np.zeros((len(Subjects), 6 * 48 * 3))
variance_array = np.zeros((len(Subjects), 6 * 48 * 3))
skewness_array = np.zeros((len(Subjects), 6 * 48 * 3))
kurtosis_array = np.zeros((len(Subjects), 6 * 48 * 3))
header_len = ""
header = ""
for subject in Subjects:
    # 新建数组
    for rawdatapath in Rawdatapaths:
        for group in Groups:
            path = rawdatapath + group
            # print(path)
            for file in os.walk(path):
                for filename in file[2]:
                    if filename.split('.')[1] == "mat":
                        if subject in filename:

                            # 读取MAT文件
                            data = scipy.io.loadmat(path + filename)
                            fnirs_oxyData = data['nirsdata']['oxyData'][0][0]
                            fnirs_dxyData = data['nirsdata']['dxyData'][0][0]
                            fnirs_totalData = data['nirsdata']['totalData'][0][0]

                            # 计算每段数据的长度
                            len_array[Subjects.index(subject), Rawdatapaths.index(rawdatapath)] = fnirs_oxyData.shape[0]
                            if Subjects.index(subject) == 0:
                                header_len = header_len + "Pr" + str(Rawdatapaths.index(rawdatapath) + 1) + ","

                            for channel_num in range(48):

                                # 计算均值
                                oxy_mean, dxy_mean, total_mean = feature_mean(fnirs_oxyData, fnirs_dxyData,
                                                                              fnirs_totalData, channel_num)
                                mean_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3] = oxy_mean
                                mean_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 1] = dxy_mean
                                mean_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 2] = total_mean


                                # 计算积分值
                                oxy_integral, dxy_integral, total_integral = feature_integral(fnirs_oxyData,
                                                                                              fnirs_dxyData,
                                                                                              fnirs_totalData,
                                                                                              channel_num,
                                                                                              Rawdatapaths.index(rawdatapath))
                                integral_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3] = oxy_integral
                                integral_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 1] = dxy_integral
                                integral_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 2] = total_integral


                                # 计算标准差
                                oxy_variance, dxy_variance, total_variance = feature_variance(fnirs_oxyData,
                                                                                              fnirs_dxyData,
                                                                                              fnirs_totalData,
                                                                                              channel_num)
                                variance_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3] = oxy_variance
                                variance_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 1] = dxy_variance
                                variance_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 2] = total_variance


                                # 计算偏度
                                oxy_skewness, dxy_skewness, total_skewness = feature_skewness(fnirs_oxyData,
                                                                                              fnirs_dxyData,
                                                                                              fnirs_totalData,
                                                                                              channel_num)
                                skewness_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3] = oxy_skewness
                                skewness_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 1] = dxy_skewness
                                skewness_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 2] = total_skewness


                                # 计算峰度
                                oxy_kurtosis, dxy_kurtosis, total_kurtosis = feature_kurtosis(fnirs_oxyData,
                                                                                              fnirs_dxyData,
                                                                                              fnirs_totalData,
                                                                                              channel_num)
                                kurtosis_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3] = oxy_kurtosis
                                kurtosis_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 1] = dxy_kurtosis
                                kurtosis_array[Subjects.index(subject), Rawdatapaths.index(
                                    rawdatapath) * 48 * 3 + channel_num * 3 + 2] = total_kurtosis


                                # 生成标题
                                if Subjects.index(subject) == 0:
                                    header = header + "Ch" + str(channel_num + 1) + "_Pr" + str(
                                        Rawdatapaths.index(rawdatapath) + 1) + "_oxy,"
                                    header = header + "Ch" + str(channel_num + 1) + "_Pr" + str(
                                        Rawdatapaths.index(rawdatapath) + 1) + "_dxy,"
                                    header = header + "Ch" + str(channel_num + 1) + "_Pr" + str(
                                        Rawdatapaths.index(rawdatapath) + 1) + "_total,"
                            # print(path + filename)
                            break
header = header[:-1]
header_len = header_len[:-1]
np.savetxt('len.csv', len_array, delimiter=',', header=header_len, comments='')
np.savetxt('mean.csv', mean_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('integral.csv', integral_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('variance.csv', variance_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('skewness.csv', skewness_array, delimiter=',', header=header, comments='', fmt='%.14f')
np.savetxt('kurtosis.csv', kurtosis_array, delimiter=',', header=header, comments='', fmt='%.14f')
print("ok")
