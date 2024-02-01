import os
from shutil import copyfile

rootdir = "D:\\fNIRS_Data\\zishu\\FC\\"
periodlist = ["1RESTING\\","2COUNT\\","3SPEAK\\","4COUNT\\","5LISTEN\\","6COUNT\\"]
grouplist = ["HC\\", "PTSD\\"]

for period in periodlist:
    for group in grouplist:
        print(rootdir+period+group)
        os.makedirs(rootdir+period+group)