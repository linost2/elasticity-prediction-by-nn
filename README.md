
# 神经网络预测晶体弹性常数

项目利用pytorch搭建简单神经网络模型，通过晶体的组成及结构信息预测晶体的21个独立弹性常数，数据来源https://materialsproject.org/) 

1.第一部分component仅从成分预测弹性常数
2.第二部分structure从成分、质量及结构（包含晶系、点群）信息预测
3.各部分包含数据爬取代码data_fetch.py,数据准备代码data_prepa.py、化学式拆解函数代码formula.py、神经网络模型计算代码main.py以及linux服务器批量计算脚本1.sh
