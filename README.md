# 时间层面分析
## 步骤
### 统一步骤
1. 修改被试列表：PTSDsub_list.csv、HCsub_list.csv
2. 读取原始数据：
   1. ReadMatRawdata.py，生成mean.csv、integral.csv、variance.csv、skewness.csv、kurtosis.csv
   2. ReadMatGLM.py，生成GLM.csv
3. 插值：chazhi.py，生成mean_chazhi.csv、integral_chazhi.csv等
4. 进入特征文件夹（如01mean），依次运行ReadCSV_mean、ReadCSV_channel_result.py、ReadCSV_roi_result.py
5. 结果保存至特征文件夹result子文件夹中
6. 参数保存至fNIRS_Py-参数子文件夹中
### 均值
1. 使用ReadMatRawdata.py读取预处理后mat格式数据，分段计算各通道oxy，dxy，total均值，保存在mean.csv中。
2. 使用chazhi.py进行缺失值填补，生成mean_chazhi.csv。
3. 组间：使用ReadCSV_mean.py进行mean_chazhi.csv读取，生成各通道不同阶段均值图片，并对每个通道每个阶段的均值进行Shapiro-Wilk 测试判断是否符合正态分布，符合正态分布进行方差齐性检验和独立样本 t 检验，否则进行Mann-Whitney U 检验。
4. 不同任务阶段之间：使用ReadCSV_mean.py进行mean_chazhi.csv读取，并对每个通道不同阶段的均值进行Shapiro-Wilk 测试判断是否符合正态分布，随后进行配对 t 检验和Wilcoxon符号秩检验。
### 积分值
将预处理后的数据进行累加
### 一般线性模型
- design_inf更新
	- 将Onset_and_Length.xlsx中对应信息填入design_inf.xlsx
	- 更新HC_Design_Inf.mat和PTSD_Design_Inf.mat
- 生成对应beta值：Task fNIRS——Individual-level Analysis
- ![image.png](https://s2.loli.net/2023/12/05/sEOQU6VMl24mC7H.png)
- 使用ReadMatGLM生成result.xlsx存放在NIRS_KIT_Individual_Analysis文件夹中
- 使用ReadGLM进行result.xlsx读取，并对每个特征进行Shapiro-Wilk 测试判断是否符合正态分布，符合正态分布进行方差齐性检验和独立样本 t 检验，否则进行Mann-Whitney U 检验。

## 参数
### 01
- HC：

| "sub01" | "sub02" | "sub03" | "sub04" | "sub05" | "sub06" | "sub07" | "sub08" | "sub09" | "sub10" | "sub11" | "sub12" | "sub13" | "sub14" | "sub15" | "sub16" | "sub17" | "sub18" | "sub19" | "sub20" | "sub21" | "sub22" | "sub23" | "sub24" | "sub25" | "sub26" | "sub27" | "sub28" | "sub29" | "sub30" | "sub31" | "sub32" | "sub33" | "sub34" | "sub35" | "sub36" | "sub37" | "sub38" | "sub39" | "sub40" | "sub41" | "sub42" | "sub43" | "sub44" |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 004     | 005     | 021     | 022     | 023     | 024     | 025     | 026     | 027     | 028     | 029     | 031     | 032     | 033     | 034     | 035     | 037     | 038     | 039     | 040     | 041     | 042     | 043     | 044     | 045     | 057     | 058     | 067     | 068     | 069     | 070     | 071     | 072     | 073     | 074     | 075     | 076     | 077     | 078     | 079     | 080     | 081     | 082     | 083     |
- PTSD：

| "sub01" | "sub02" | "sub03" | "sub04" | "sub05" | "sub06" | "sub07" | "sub08" | "sub09" | "sub10" | "sub11" | "sub12" | "sub13" | "sub14" | "sub15" | "sub16" | "sub17" | "sub18" | "sub19" | "sub20" | "sub21" | "sub22" | "sub23" | "sub24" | "sub25" | "sub26" | "sub27" | "sub28" | "sub29" | "sub30" | "sub31" |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 006     | 007     | 008     | 009     | 010     | 011     | 013     | 015     | 016     | 017     | 018     | 019     | 020     | 046     | 047     | 048     | 049     | 051     | 053     | 054     | 055     | 056     | 059     | 060     | 061     | 062     | 063     | 064     | 065     | 084     | 085     |


- roi：

| Pre-Motor and Supplementary Motor Cortex | Dorsolateral prefrontal cortex | Frontopolar area | Orbitofrontal area | Middle Temporal gyrus | Superior Temporal Gyrus | Temporopolar area | Subcentral area | pars opercularis_ part of Broca's area | pars triangularis Broca's area | Dorsolateral prefrontal cortex2 | Inferior prefrontal gyrus | Retrosubicular area |
| ---------------------------------------- | ------------------------------ | ---------------- | ------------------ | --------------------- | ----------------------- | ----------------- | --------------- | -------------------------------------- | ------------------------------ | ------------------------------- | ------------------------- | ------------------- |
| 19                                       | 42                             | 8                | 7                  | 1                     | 18                      | 3                 | 20              | 46                                     | 5                              | 10                              | 4                         | 17                  |
| 38                                       | 44                             | 25               | 9                  | 2                     | 35                      | 12                | 36              | 47                                     | 22                             | 21                              | 6                         | 34                  |
| 48                                       |                                | 26               | 11                 | 13                    |                         | 14                |                 |                                        | 24                             | 23                              |                           |                     |
|                                          |                                | 27               |                    | 15                    |                         |                   |                 |                                        | 31                             | 29                              |                           |                     |
|                                          |                                | 28               |                    | 16                    |                         |                   |                 |                                        | 32                             | 30                              |                           |                     |
|                                          |                                |                  |                    | 33                    |                         |                   |                 |                                        | 37                             | 40                              |                           |                     |
|                                          |                                |                  |                    |                       |                         |                   |                 |                                        | 39                             | 41                              |                           |                     |
|                                          |                                |                  |                    |                       |                         |                   |                 |                                        |                                | 43                              |                           |                     |
|                                          |                                |                  |                    |                       |                         |                   |                 |                                        |                                | 45                              |                           |                     |


## 结果
### 01
#### 均值结果
| 分通道结果     |               |                     |                        |
| -------------- | ------------- | ------------------- | ---------------------- |
| 任务间总显著性 |               |                     |                        |
| 类别           | 配对t检验显著 | 配对t检验显著且正态 | Wilcoxon符号秩检验显著 |
| PSTD           | 125           | 13                  | 232                    |
| HC             | 384           | 9                   | 419                    |
| 组间总显著性   |               |                     |                        |
| PSTD+HC        | 43            | 2                   | 33                     |

| 分脑区结果     |               |                     |                        |
| -------------- | ------------- | ------------------- | ---------------------- |
| 任务间总显著性 |               |                     |                        |
| 类别           | 配对t检验显著 | 配对t检验显著且正态 | Wilcoxon符号秩检验显著 |
| PSTD           | 33            | 2                   | 60                     |
| HC             | 155           | 15                  | 177                    |
| 组间总显著性   |               |                     |                        |
| PSTD+HC        | 12            | 1                   | 12                     |
#### 积分值结果

| 分通道结果     |               |                     |                        |
| -------------- | ------------- | ------------------- | ---------------------- |
| 任务间总显著性 |               |                     |                        |
| 类别           | 配对t检验显著 | 配对t检验显著且正态 | Wilcoxon符号秩检验显著 |
| PSTD           | 152           | 19                  | 233                    |
| HC             | 381           | 18                  | 389                    |
| 组间总显著性   |               |                     |                        |
| PSTD+HC        | 53            | 7                   | 40                     |

| 分脑区结果     |               |                     |                        |
| -------------- | ------------- | ------------------- | ---------------------- |
| 任务间总显著性 |               |                     |                        |
| 类别           | 配对t检验显著 | 配对t检验显著且正态 | Wilcoxon符号秩检验显著 |
| PSTD           | 36            | 0                   | 59                     |
| HC             | 135           | 8                   | 151                    |
| 组间总显著性   |               |                     |                        |
| PSTD+HC        | 13            | 1                   | 11                     |
# 空间层面分析
## 均值
### HC
![057.png](https://s2.loli.net/2023/12/14/AvC8omN9p73R1JG.png)

![057.png](https://s2.loli.net/2023/12/14/yYnJfE1p9TxkPaA.png)

### PTSD
![054.png](https://s2.loli.net/2023/12/14/IH91ok3WntOqVPr.png)

![054.png](https://s2.loli.net/2023/12/14/GtIKJ24RclSLTio.png)

## 功能连接
## ALFF