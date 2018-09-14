# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 21:20:08 2018
@title：求可达性矩阵及强分图
@author: ff7f
"""
from 矩阵类 import *
#q = "已知邻接矩阵\n{A}，求可达性矩阵P，并找出所有强分图。"
n = input('> 随机生成邻接矩阵，请输入矩阵阶数：')
while n:
    A = genMatrix(int(n))   # 随机生成邻接矩阵A
    print(f"【例】已知邻接矩阵A：\n{A}\n求可达性矩阵P，并找出所有强分图。")
    funcs = [strongSubGraph]   # 计算强分图函数
    flowCalc(A, *funcs)
    #pageRank(A)   #pageRank算法求结点权重
    n = input('> 请输入矩阵阶数：')

















"""
import  numpy as np
strong1 = np.mat([
[0, 1, 1, 0],
[0, 0, 0, 0],
[0, 1, 0, 1],
[1, 1, 0, 0]])

flowCalc(strong1, *funcs)
"""