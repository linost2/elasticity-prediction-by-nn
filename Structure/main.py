# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:55:29 2022

@author: youlin zhu
"""
import pickle
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import sys
import numpy as np
from sklearn.model_selection import train_test_split

#定义训练函数、搭建模型、相关参数设置
def train(m, x, y,  max_iter=10000):
    criterion = nn.SmoothL1Loss()
    optimizer = torch.optim.Adam(m.parameters(),lr=0.001)
    loss_hist = []
    R2_hist = []
    y_bar = torch.mean(y, 0)

    for t in range(1, max_iter + 1):
        y_pred = m(x)
        loss = criterion(y_pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if t % 1000 == 0:
            loss_hist.append(loss.detach())
            R2 = 1 - torch.sum((y - y_pred)**2, 0) / torch.sum((y - y_bar)**2, 0)
            R2 = torch.mean(R2)
            R2_hist.append(R2.detach())
            print(f'epoch: {t}, loss: {float(loss.item()):.4f}, R^2: {float(R2):.4f}')
            if len(loss_hist) > 2 and torch.abs((loss_hist[-1]-loss_hist[-2])/loss_hist[-1]) < 1e-6:
                break
    return m, loss_hist, R2_hist
    
#定义评估绘图函数
def evalu(Y_true,Y_pred,name):
    c2=['#79B5E1','#FF8C7A','#fecf45','#b8f1cc']  
    for i in range(21):
        Y_bar = np.mean(Y_true[:,i]) 
        R_2 = 1 - np.sum((Y_true[:,i] - Y_pred[:,i])**2) / np.sum((Y_true[:,i] - Y_bar)**2)
        plt.plot(Y_true[:, i], Y_pred[:, i], '.',color=c2[1])
        plt.plot(Y_true[:, i], Y_true[:, i], '-',color=c2[2])
        plt.xlabel('True')
        plt.ylabel('Predicted')
        print(name+f'_c{[i]}, R^2={R_2:.4f}')
        plt.title(name+f'_c{[i]}, R^2={R_2:.4f}')
        plt.savefig(name+f'_c{i}.png', dpi=100)
        plt.clf()
        # plt.show()
       
        # plt.pause(1)
        # plt.close()

#%%

#定义读取函数
def main(layer1,layer2,layer3):
    with open("Matrix_input.pkl", mode="rb") as opened_file:
        X = pickle.load(opened_file)
    with open("Matrix_output.pkl", mode="rb") as opened_file:
        Y = pickle.load(opened_file)
#%%
#模型搭建及数据读取
    m = nn.Sequential(nn.Linear(122, layer1), nn.ReLU(), nn.Linear(layer1, layer2), nn.ReLU(), nn.Linear(layer2, layer3), nn.ReLU(), nn.Linear(layer3, 21))
    m.double()   
    print(layer1,layer2,layer3)

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.2, random_state = 23)
    
    X_train = torch.tensor(np.array(X_train))
    X_test = torch.tensor(np.array(X_test))
    
    Y_train = torch.tensor(np.array(Y_train))
    Y_test = torch.tensor(np.array(Y_test))

 #训练开始、评估  
    m,loss_hist,R2_hist= train(m, X_train, Y_train, max_iter=100000)

    with torch.no_grad():
        Y_pred_train = m(X_train).numpy()
        Y_true_train = Y_train.numpy()
        Y_pred_test = m(X_test).numpy()
        Y_true_test = Y_test.numpy()

    evalu(Y_true_train,Y_pred_train,'train')
    evalu(Y_true_test,Y_pred_test,'test')
    
   
if __name__ == "__main__":
#接受shell 传入的参数， 便于批量计算
    main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
