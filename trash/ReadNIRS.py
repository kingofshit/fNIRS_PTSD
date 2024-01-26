import mne
from mne_nirs import read_nirs

fnirs_raw_dir = "D:\\fNIRS_Data\\zishu\\raw\\ptsd\\066_WANGAN"
filename = "通用_2024-01-02_09-27-22_PTSD066_yiyuan_女_1980-01-01_.nirs"
# 加载.nirs数据
raw = read_nirs(fnirs_raw_dir + filename)
print("1")
# 然后可以对数据进行进一步处理或分析