# 设置工作目录为指定的路径
setwd("C:/Users/wjy/OneDrive - hdu.edu.cn/研究生/大论文/fNIRS_Py/figs/FC")
library(corrplot)
example_data1<-read.csv("004.txt",row.names="p1",sep='\t')#读取数据
example_data1 =data.matrix(example_data1)# data frame转换为矩阵
P1<-corrplot(example_data1,
	method="circle",# 显示为圆形
	type="upper",# 只显示左上角
	addCoef.col="white",# 填充数字的颜色
	number.cex=0.7,# 填充的数字的大小
	tl.cex =0.8,#标签字体大小
	tl.col="black",#标签字体颜色
	tl.srt=0
	)
P1