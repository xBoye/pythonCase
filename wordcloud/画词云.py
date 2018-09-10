# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 00:07:09 2018
@title：画词云
@author: ff7f
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image
import re

#1。读入文本
filename = '七律.txt'

with open(filename, encoding='utf8') as f:
    text = f.read()
    s_train = text.split('\n\n') 

train_size = len(s_train)   # 训练集文档数: 

#2. 所有特征词集tokens
tokens = []    # 文档特征词
for s in s_train:
    body = s.split('\n')[1]
    sentences = re.split('[，。？；]',body)[:-1]
    words = []
    for x in sentences:
        # 七律每句分词格式(12, 34, 56, 67)，每句分成4个词
        words.extend([x[:2],x[2:4],x[4:6],x[5:]])
    tokens.extend(words)
tokens_size = len(tokens)    # 词汇数量

print(f'> 文档数：{train_size} 词汇数：{tokens_size}')  

#3. 画词云
logo = 'logo2.png'
def drawc(corpus=None,shape=logo,palette=logo,name=None):
    #特征词画词云:corpus:空格连接tokens
    if name is not None:
        imgout = '%s词云图.png' % name
    else:
        imgout = '词云图2.png'
    img_shape = np.array(Image.open(shape))
    #print(img_shape.shape)
    render_color = np.array(Image.open(palette))
    #print(render_color.shape)
    plt.figure(figsize=(11,11))
    #plt.title('the Daos')
    mywc = WordCloud(
       background_color="white", 
       max_words=800,
       mask=img_shape,
       max_font_size=30, 
       min_font_size=1,
       font_path="hylsf.ttf")
    mywc.generate(' '.join(corpus))
    #显示词云
    image_colors = ImageColorGenerator(render_color)
    plt.imshow(mywc.recolor(color_func=image_colors))
    plt.imshow(mywc)
    plt.axis("off")
    plt.show()

    mywc.to_image().save(imgout)  #词云存为文件
    
#main
drawc(tokens)  #画词云

