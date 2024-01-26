import csv
import os

pathlist = [r'C:\Users\wjy\OneDrive - hdu.edu.cn\研究生\大论文\fNIRS_Py\mni']
Data = {}
Data.fromkeys(['Group', 'NO.', 'START_1', 'END_1', 'START_2', 'END_2', 'START_3', 'END_3',
               'START_4', 'END_4', 'START_5', 'END_5', 'START_6', 'END_6'])
Data['Group'] = []
Data['NO.'] = []
for i in range(6):
    Data['START_' + str(i+1)] = []
    Data['END_' + str(i + 1)] = []

for path in pathlist:
    for file in os.walk(path):
        for filename in file[2]:
            if filename.split('.')[1] == "csv":
                print(path + filename)
                with open(path + filename, 'r') as f:
                    csvdata = csv.reader(f)
                    row_num = 0
                    period = 0
                    isappendArray = [0, 0, 1, 1]
                    isappend_index = 0
                    for row in csvdata:
                        row_num = row_num + 1
                        for period_num in range(6):
                            # print('\'' + str(period_num +1) + '\'')
                            if str(period_num +1) in row:
                                period = period_num +1
                                # print(row)
                        isappend = isappendArray[isappend_index]
                    if row_num != 25:
                        print(row_num)
# mylist = ['1']
# if ('\'' + str(1) + '\'') in mylist:
#     print('yes')
# if ('\'' + str(1) + '\'') == '1':
#     print('yyy')