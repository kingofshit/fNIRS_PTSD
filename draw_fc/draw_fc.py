import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

up = 1
down = -1
# filelist = ["HC_Count1_FC_CHANNEL","PTSD_Count1_FC_CHANNEL",
#             "HC_Count2_FC_CHANNEL","PTSD_Count2_FC_CHANNEL",
#             "HC_Count3_FC_CHANNEL","PTSD_Count3_FC_CHANNEL",
#             "HC_Listen_FC_CHANNEL","PTSD_Listen_FC_CHANNEL",
#             "HC_Resting_FC_CHANNEL","PTSD_Resting_FC_CHANNEL",
#             "HC_Speak_FC_CHANNEL","PTSD_Speak_FC_CHANNEL"]
filelist = ["SUB_Count1_FC_CHANNEL",
            "SUB_Count2_FC_CHANNEL",
            "SUB_Count3_FC_CHANNEL",
            "SUB_Listen_FC_CHANNEL",
            "SUB_Resting_FC_CHANNEL",
            "SUB_Speak_FC_CHANNEL"]


def draw_fc(vmin, vmax, path):
    data = pd.read_csv(path, sep='  ', header=None)
    print(np.array(data).max())
    print(np.array(data).min())
    # 绘制热力图
    channel = [i for i in range(1, 49)]
    sns.heatmap(data, cmap='coolwarm', annot=False, center=0, vmin=vmin, vmax=vmax, fmt=".2f", linewidths=.5, xticklabels=False,yticklabels=False)
    # plt.xlabel("Columns")
    # plt.ylabel("Columns")
    # plt.title("Correlation Heatmap")

    # 显示图形
    # plt.show()
    plt.savefig(filename+".jpg")
    plt.close()


for num in range(len(filelist)):
    filename = filelist[num]
    path = r"C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\draw_fc"
    draw_fc(down, up, path+"\\"+filename+".txt")
