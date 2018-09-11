# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 19:20:26 2018
@title: 矩阵类
@author: ff7f
@判断是否是子集or超集：set1.issubset(set2)  or set1.issuperset(set2)
"""
import random
import numpy as np
from scipy.spatial import distance as dist  #距离函数
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片

def str2mat(s,dim=None):
    #由01串转为order阶矩阵
    if dim is None:
        dim = int(np.sqrt(len(s)))
        _row, _col = dim, dim
    elif isinstance(dim, int):
        _row, _col = dim, dim
    elif isinstance(dim, tuple):
        if len(dim)==2:
            _row, _col = dim
        else:
            return False
    if _row*_col == len(s):
        return  np.mat(' '.join(s)).reshape(_row, _col)
    else:
        return False

def mPowers(A):
    '''计算邻接矩阵A: 0次幂到n次幂（方阵）'''
    n = int(A.shape[0])
    E = np.mat(np.eye(n),dtype='int64')
    powers = [E,A]   #Al：邻接矩阵A各次幂列表
    for i in range(2,n+1):
        powers.append(np.mat(np.where(A**i,1,0)))

    print(*map(repr,powers),sep='\n')
    return powers

def bis2mat(s):
    #由01串转为order阶矩阵
    n = int(np.sqrt(len(s)))
    if n*n==len(s):
        return  np.mat(' '.join(s)).reshape(n,n)
    else:
        return False
		

def showImg(imgfile,size=(9,9)):
    #显示图片
    img = mpimg.imread(imgfile) # 读取图片文件
    #print('shape:', img.shape)  #图片形状
    plt.figure(figsize=size)
    plt.imshow(img) # 显示图片
    plt.axis('off') # 不显示坐标轴
    plt.show()

def subtract(L1,L2):
    #列表减法L1-L2
    return [x for x in L1 if x not in L2]

def elistRepeat(L1):
    #列表消重
    return [x for x in map(eval,set(map(str,L1)))]

def eltupleRepeat(ltuple,idx):
    #元组列表按索引idx分量相同消重
    values = []
    results = []
    for lt in ltuple:
        if lt[idx] not in values:
            values.append(lt[idx])
            results.append(lt)
    return results

def list_add(L1,a):
    #列表L1添加元素a,如果列表中不存在a,则添加;否则不添加
    if a not in L1:
        L1.append(a)
    return L1

def ltuple_add(ltuple,a,idx):
    #元组列表添加元素，若a[idx]值已存在，则不添加
    values = [x for x in map(lambda item:item[idx],ltuple)]
    if a[idx] not in values:
        ltuple.append(a)
    return ltuple

def showMatrix(A, description=''):
    #显示矩阵A
    print('> 邻接矩阵A%s\n' % description, '\n'.join(map(repr,A.tolist())),sep='')

def genMatrix(order=4,rate=0.1):
    #随机生成阶数为order的邻接矩阵，rate：1的几率
    datum = list((('1'*int(rate*10)).ljust(10,'0')))  #按rate生成基准序列
    random.shuffle(datum)
    s = ''
    while len(s)<order**2:
        row = ''.join([random.choice(datum) for i in range(order)])
        if '1' not in row:
            continue
        s += row
    A = np.mat(' '.join(list(s))).reshape(order,order)   #M邻接矩阵
    #showMatrix(A)
    #print('$ 随机生成%s阶邻接矩阵A：\n' % order,'\n'.join(map(repr,A.tolist())),sep='')
    return A

def genE(order=5):
    #生成单位方阵
    E = np.matrix(np.eye(order,dtype=int))
    return E

def 矩阵幂(A):
    '''计算邻接矩阵A: 1到n次幂（方阵）'''
    n = int(A.shape[0])
    E = np.mat(np.eye(n),dtype='int64')
    powers = [E,A]   #Al：邻接矩阵A各次幂列表
    for i in range(2,n+1):
        powers.append(np.mat(np.where(A**i,1,0)))
        print('> A%d = A**%d\n' % (i,i),repr(powers[i]),sep='')
    #print(*map(repr,powers),sep='\n')
    return powers

def 可达性矩阵(powers):
    '''计算可达性矩阵,powers：矩阵各阶幂列表：0次到n次幂'''
    P = powers[1]
    for A in powers[2:]:
        P |= A
    print('> 可达性矩阵P = A ∨ A2 ∨ ... ∨ An\n',repr(P),sep='')  # | 逻辑或运算
    #print('> 可达性矩阵(P)\n','\n'.join(map(repr,P.tolist())),sep='')
    return P

def 互达矩阵(P):
    '''输出相互可达矩阵P^P.T，参数P为可达性矩阵'''
    
    X = P & P.T
    print('> 可达性矩阵转置矩阵P.T\n',repr(P.T),sep='')
    print("> 相互可达矩阵(P^P.T)\n",'\n'.join(map(repr,X.tolist())),sep='')
    return X

def 单向可达矩阵(P):
    #单向可达矩阵
    return P | P.T

def reachabilityMatrix(A):
    #由邻接矩阵A求可达性矩阵P
    P = 可达性矩阵(矩阵幂(A))
    X = 互达矩阵(P)
    return P,X

def maxSubGraph(X,label='v'):
    '''求最大分图，参数X：可达矩阵'''
    S = []  #分图s
    for i in range(X.shape[0]):
        node = '%s%s' % (label,i+1)
        si = {node,}  #{i+1,}  #结点i所在分图
        for j in range(X.shape[1]):
            if X[i,j]:
                node = '%s%s' % (label,j+1)
                si.add(node)   #(j+1)
            #print('X[%d,%d]=' % (i,j),X[i,j])
        if si not in S:
            S.append(si)
    #print('$ 所有分图\n','，'.join(map(repr,S)),sep='')
    return S

def strongSubGraph(A,label='v'):
    #求邻接矩阵A所包含的强分图，返回强分图列表strongs
    strongs = maxSubGraph(互达矩阵(可达性矩阵(矩阵幂(A))))
    print('> 所有强分图(相互可达矩阵中找出所有双向可达的最大结点子集就是强分图)\n','，'.join(map(repr,strongs)),sep='')
    return strongs

def getNodeReachableList(P):
    #根据可达矩阵计算节点可达列表
    rel = []  #分图s
    for i in range(P.shape[0]):
        nodi = {i+1,}  #结点i可达集
        for j in range(P.shape[1]):
            if P[i,j]:
                nodi.add(j+1)
        rel.append((i+1,nodi))
    #print('\n$ 结点可达集\n','\n'.join(map(repr,rel)),sep='')
    return rel

def isReachable(x,y,P):
    #判断结点x,y是否可达,P可达性矩阵
    return True if P[x-1,y-1] or P[y-1,x-1] else False

def singleSubGraph(A):
    #求A的单向分图
    reachlist = getNodeReachableList(单向可达矩阵(可达性矩阵(矩阵幂(A))))  #计算结点可达列表
    singles = eltupleRepeat(reachlist,1)
    #print(singles)
    done = False
    while not done:
        oldsingles = singles[:]
        for node_i in singles:   #reachlist
            for node_j in singles:  #reachlist:
                if node_i[1] != node_j[1] and node_i[1].issuperset(node_j[1]):
                    if node_i in singles:
                        singles.remove(node_i)
                    difset = node_i[1]-node_j[1]
                    difset.add(node_i[0])
                    ltuple_add(singles,(node_i[0],difset),1)
            #print(singles)        
        if oldsingles == singles:
            done = True
    singles = list(map(lambda item:item[1],singles))
    print('\n$ 所有单向分图\n',','.join(map(repr,singles)),sep='')
    return singles

def weakSubGraph(A):
    #求A弱分图，A|A.T求可达性矩阵
    weaks = maxSubGraph(互达矩阵(可达性矩阵(矩阵幂(A|A.T))))
    print('\n$ 所有弱分图\n','，'.join(map(repr,weaks)),sep='')
    return weaks

def pageRank(M, a=0.85, error=1e-8):
    #网页排名算法M:邻接矩阵，a:阻尼系数，error:迭代误差
    n,_ = M.shape
    Mp = np.zeros((n,n))   #链接概率矩阵
    for i,m in enumerate(M):
        Mp[i] = m/m.sum()   #每行归一化
             
    P = Mp.T   #P概率转移矩阵
    A = a*P+(1-a)*np.ones((n,n))/n  #A改进概率转移矩阵
    v = np.mat(np.ones((n,1))/n)
    vx = A*v   #向量迭代公式
    i = 0    #i迭代次数
    while dist.euclidean(vx,v) > error:   #欧氏距离迭代误差比较
        v = vx    #大于误差继续迭代
        vx = A*v
        i += 1
    
    print('\nPageRank迭代出邻接矩阵各节点权重(降序排列)')
    lvx = vx.T.tolist()[0]
    weights = {}
    for i,x in zip(range(n),lvx):
        weights.setdefault(str(i+1),x)
        #print('节点%02d的权重 : %s' % (i+1,x))
    print('\n'.join(map(lambda item:'节点[%s]权重：%s' % (item[0].rjust(2,'0'),item[1]),sorted(weights.items(),key=lambda item:item[1],reverse=True))))
    return weights

 
def flowCalc(Adj,*funcs):
    #计算流，参数：邻接矩阵A
    if isinstance(Adj, list):
        for A in Adj:
            list(map(lambda f:f(A), funcs))
    else:
        list(map(lambda f:f(Adj),funcs))
        
#list(map(lambda A:flowCalc(A , *funcs), Adjs))

class AdjMatrix():
    #邻接矩阵类
    def __init__(self,):
        pass

"""
def main():
    n = input('> 请输入矩阵阶数：')
    while n:
        A = genMatrix(int(n))
        
        pageRank(A)   #验证pageRank网页排名算法
        n = input('> 请输入矩阵阶数：')

if __name__ == '__main__':
    #求可达性矩阵
    #showImg('e:\\implib\\li832.png')   #adj_1_A的图
    showImg('png\\图例2.png',size=(4,4))
    #Adjs = [li832_A]   #[adj_1_A, li832_A, tu829_A]
    
    A_example1 = np.mat([[0,1,1,1],[0,0,0,1],[0,1,0,0],[0,0,1,0]])
    A_example2 = np.mat([[0,1,1,0],[0,0,0,0],[0,1,0,1],[1,1,0,0]])
    Adjs = [A_example2]
    discriptions = ['adj_1_A', 'li832_A', 'tu829_A']
    #list(map(lambda item:showMatrix(*item), zip(Adjs,discriptions)))  #显示邻接矩阵
    funcs = [showMatrix,strongSubGraph]
    #tags = ['强分图','单向分图','弱分图']
    #funcs = [strongSubGraph,singleSubGraph,weakSubGraph]
    list(map(lambda A:flowCalc(A , *funcs), Adjs))
    #main(flowCalc,*funcs)
"""
#main
if __name__ == '__main__':
    main()

