# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 21:46:19 2018
@title：查找两首最相似的诗
@author: ff7f
"""
"""
数据集： 七律.txt
测试集： cases.txt   # 建立一个小型的子集进行算法测试

处理流程：
1.读入文本，生成诗列表；
2.分词，基于诗文文言的特殊性，使用12,34,56,67格式进行分词；
3.文档向量化，使用tfidf向量方法；
4.循环计算余弦相似度，生成相似字典或矩阵；
5.根据相似矩阵，找出最相似的两首诗。
"""
import re
from tqdm import tqdm  # 进度条

#1。读入文本
filename = '七律.txt'
with open(filename, encoding='utf8') as f:
    text = f.read()
    s_train = text.split('\n\n')  
#print(f'> 诗数：{len(s_train)}')  #诗数：总32196首


#2. 忽略标题作者，诗正文分词，生成特征词集tokens和空格连接特征词语料corpus
print('> 生成语料')
tokens = []    # 文档特征词
corpus = []    # 特征词用空格连接语料
for s in s_train:
    body = s.split('\n')[1]
    sentences = re.split('[，。？；]',body)[:-1]
    sentence = ''
    words = []
    for x in sentences:
        # 七律每句分词格式(12, 34, 56, 67)，每句分成4个词
        words.extend([x[:2],x[2:4],x[4:6],x[5:]])
        sentence = ' '.join(words)   # 空格连接特征词
    tokens.append(words)
    corpus.append(sentence[:])

#print(corpus)

#3. 文档计算tfidf向量权重矩阵，生成词汇表
#重要属性与函数：
#tv_model.get_feature_names()  # 获取特征词
#tv_model.vocabulary_  # 词汇表
#vecs.size   # 特征向量总长度
#vecs.shape  # 特征向量矩阵维数
from sklearn.feature_extraction.text import TfidfVectorizer as TV #tfidf向量

model = TV()  #tfidf向量
vecs_train = model.fit_transform(corpus)   # 稀疏矩阵 防止溢出 生成特征向量矩阵，每行对应一首诗，每列对应一个特征词
vocab_train = model.get_feature_names()
vocab_size = len(vocab_train)   # 词汇表size
#print(f'  词汇表size：{vocab_size}')

import numpy as np
# 数据量大，计算余弦相似度速度很慢，随机取一个批次进行计算
train_size = len(s_train)   # 训练集size: 总32196首
batch_size = 200            # 批次包含文档数

batch_mask = np.random.choice(train_size, batch_size, replace=False)    # 随机抽取batch_size首
vecs = vecs_train[batch_mask]

#4.计算余弦相似度，生成相似字典，数据集大，余弦相似度速度慢，corpus取子集测试
from scipy.spatial.distance import cosine

print('> 正在计算相似度，请稍等。。')
n = batch_size  #文档数
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

# 显示结果print(f'  ')
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
