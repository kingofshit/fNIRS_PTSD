import os
from shutil import copyfile

pathlist = ["D:\\fNIRS_Data\\zishu\\NIRS_KIT_RESTING\\HC\\", "D:\\fNIRS_Data\\zishu\\NIRS_KIT_RESTING\\PTSD\\"]

for path in pathlist:
    for file in os.walk(path):
        for filename in file[2]:
            if filename.split('.')[1] == "mat":
                source = path + filename
                target = path + filename.split('.')[0] + "\\" + filename
                print(target)
                os.makedirs(path + filename.split('.')[0] + "\\")
                copyfile(source, target)
