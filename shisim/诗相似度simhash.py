# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:46:19 2018
@title：查找两首最相似的诗-使用simhash
@author: ff7f
"""
"""
训练数据集： 七律.txt
处理流程：
1.读入文本，生成诗列表；
2.分词，基于七律诗特点，按12,34,56,67格式进行分词；
3.文档向量化，使用tfidf向量方法；
4.计算simhash，两两计算hamming距离，生成相似字典；
5.相似字典数据按相似度逆序排列，找出最相似的两首诗。
"""
import re
import numpy as np
from tqdm import tqdm  # 进度条

#1。读入文本
filename = '七律.txt'
with open(filename, encoding='utf8') as f:
    text = f.read()
    s_train = text.split('\n\n')  

train_size = len(s_train)   # 训练集文档数: 
#print(f'> 诗数：{train_size}')  


#2. 忽略标题作者，诗正文分词，生成特征词集tokens和空格连接特征词语料corpus
print('> 生成语料')
tokens = []    # 文档特征词
corpus = []    # 特征词用空格连接语料
for s in s_train:
    body = s.split('\n')[1]
    sentences = re.split('[，。？；]',body)[:-1]
    #sentence = None
    words = []
    for x in sentences:
        # 七律每句分词格式(12, 34, 56, 67)，每句分成4个词
        words.extend([x[:2],x[2:4],x[4:6],x[5:]])
    #sentence = ' '.join(words)   # 空格连接特征词
    tokens.append(words)
    corpus.append(' '.join(words))


#3. 计算simhash
from simhash import Simhash
import os
import pickle

simfile = 'simcodes.pkl'
if not os.path.exists(simfile):
    print('> 正在计算simhash，请稍等。。')
    simcodes = []
    for _token in tqdm(tokens):
        simcode = Simhash(_token).value
        simcodes.append(simcode)
    with open(simfile, 'wb') as f:
        pickle.dump(simcodes, f)

simcodes = np.load(simfile)

#4. 随机获取tokens批数据
batch_size = 2000           # 批次包含文档数
batch_mask = np.random.choice(train_size, batch_size, replace=False)    

#5.计算hamming距离
def hamming(u, v):
    # 计算hamming距离
    x = u ^ v
    dist = 0
    while x:
        dist += 1
        x &= x - 1
    return dist

print('\n\n> 计算hamming距离..')
n = batch_size
simDict = {}
for i in tqdm(range(n-1)):
    for j in range(i+1,n):
        dist = hamming(simcodes[batch_mask[i]], simcodes[batch_mask[j]])
        simDict.setdefault('第%s-%s首' % (batch_mask[i],batch_mask[j]),dist)

#6. 根据相似矩阵，找出最相似两首诗
f = lambda item:item[0].ljust(5) + ' 海明距离：'+str(item[1])
simDict_sorted = sorted(simDict.items(),key=lambda item:item[1])
result = list(map(f, simDict_sorted))
# 显示TOP3
top_n = 2
print(f'\n\n> simhash最相似TOP{top_n} [总文档数：{train_size}，批次文档数：{batch_size}]')
for t in range(top_n):
    i,j = map(int,re.findall('\d+',simDict_sorted[t][0])) 
    print(f'> {result[t]}')
    print(f'> 第{i}首诗\n{s_train[i]}')
    print(f'> 第{j}首诗\n{s_train[j]}')

#print(f'\n> 随机抽取文档列表：\n{batch_mask}')


#7. 输出相似度计算结果
outfile='hamsim.txt'
with open(outfile,'w',encoding='utf8') as fout:
    print(f'> 总文档数：{train_size}，批次文档数：{batch_size}', file=fout)
    print('> simhash相似度计算结果(海明距离)：',file=fout)
    print('\n'.join(result),file=fout)
    print('\n随机抽取文档列表：\n{batch_mask}', file=fout)













"""
#3. 文档计算tfidf向量权重矩阵，生成词汇表
#重要属性与函数：
#tv_model.get_feature_names()  # 获取特征词
#tv_model.vocabulary_  # 词汇表
#vecs.size   # 特征向量总长度
#vecs.shape  # 特征向量矩阵维数
from sklearn.feature_extraction.text import TfidfVectorizer as TV #tfidf向量

model = TV()  #tfidf向量
vecs_train = model.fit_transform(corpus)   # 稀疏矩阵 防止溢出 特征向量矩阵，每行对应一首诗，每列对应一个特征词
vocab_train = model.get_feature_names()
vocab_size = len(vocab_train)   # 词汇表size
#print(f'  词汇表size：{vocab_size}')

import numpy as np
# 数据量大，计算余弦相似度速度很慢，随机取一个批次进行计算
#train_size = len(s_train)   # 训练集size: 总32196首
batch_size = 5            # 批次包含文档数

batch_mask = np.random.choice(train_size, batch_size, replace=False)    
vecs = vecs_train[batch_mask]   # 从特征向量矩阵随机抽取batch_size首

#4.计算余弦相似度，生成相似字典，数据集大，余弦相似度速度慢，corpus取子集测试
from scipy.spatial.distance import cosine

print('> 正在计算相似度，请稍等。。')
n = batch_size  # 批次文档数
simDict = {}   # 相似度字典结构
for i in tqdm(range(n-1)):      # tqdm显示进度条
    for j in range(i+1, n):
        sim = 1-cosine(vecs[i].toarray(),vecs[j].toarray())  #相似度.toarray()
        simDict.setdefault('第%s-%s首' % (batch_mask[i],batch_mask[j]),sim)

#5. 根据相似字典，找出最相似的2首诗
f = lambda item:item[0].ljust(5) + ' 相似度：'+str(item[1])
simDict_sorted = sorted(simDict.items(),key=lambda item:item[1],reverse=True)
i,j = map(int,re.findall('\d+',simDict_sorted[0][0])) 
result = list(map(f, simDict_sorted))

# 显示结果
print(f'\n\n> 训练集size：{train_size}，词汇表size：{vocab_size}，本批文档数：{batch_size}')
print(f'> 最相似的两首诗：{result[0]}')
print(f'> 第{i}首诗  {s_train[i]}')
print(f'> 第{j}首诗  {s_train[j]}')
print(f'> 随机抽取文档列表：\n{batch_mask}')

#6. 结果存入文件
outfile = 'cossim.txt'
with open(outfile,'w',encoding='utf8') as fout:
    print(f'> 训练集size：{train_size}，词汇表size：{vocab_size}，本批文档数：{batch_size}\n随机抽取文档列表：\n{batch_mask}', file=fout)
    print('> 相似度计算结果：',file=fout)
    print('\n'.join(result),file=fout)
"""