# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 22:35:31 2018
@title: 半结构化文本倒库
@author: ff7f
"""
import sqlite3
import re
import os
import sys

def text2sqlite3(textfile):
    # 文本倒库
    dbname = 'shi.db'
    if os.path.exists(dbname):
        try:
            os.remove(dbname)
        except Exception as e:
            print(e)
            sys.exit()
    # 创建基本表
    sql_create_table = """create table shi(
          id integer primary key autoincrement,
          title varchar(50),
          author varchar(20),
          dynasty varchar(10),
          body text)"""
    # 插入数据
    sql_insert_data = """insert into shi(title, author, dynasty, body) values (?,?,?,?)"""
    # 查询数据
    sql_select_data = """select * from shi"""
    try:
        c = sqlite3.connect(dbname)
        cx = c.cursor()
        cx.execute(sql_create_table)   # 创建基本表
        with open(textfile, encoding='utf8') as f:
            shies = f.read().split('\n\n')
            # print(shies)
    
        for index, shi in enumerate(shies):
            # print(index, shi)
            shi = shi.replace('　', '')
            title, dynasty, author, body = re.search('《([\w、·：《》□【】\—\{\}…]*)》(\w+)·(\w+)\n(.+)', shi).groups()
            tuple = (title, author, dynasty, body)
            #print(f'标题：{title}  作者：{author}  朝代：{dynasty}\n正文：{body}\n')
            #print(index, tuple)
            cx.execute(sql_insert_data, tuple)
            
        # 查询数据
        print('查询数据..')
        cx.execute(sql_select_data)
        data = cx.fetchall()
        for t in data:
            print(t)
    except Exception as e:
        print(e)
    finally:
        cx.close()
        c.commit()
        c.close()

#main
if __name__ == '__main__':
    test = 0
    if test:
        textfile = "test.txt"
    else:
        textfile = "五绝.txt"
    text2sqlite3(textfile)
    
