# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:55:24 2018
@title：examples
@author: lenovo
"""
import sqlite3
class DB:
    # DB类
    def __init__(self, dbname):
        
        #assert os.path.exists(dbname), '数据库不存在！' 
        self.dbname = dbname
        self.con = None
        self.cur = None
        
        self.open()
        
    def open(self):
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()
    
    def select(self, sql, args=None):
        if args:
            self.cur.execute(sql % args)
        else:
            self.cur.execute(sql)
        result = '\n'.join(map(repr,self.cur.fetchall()))
        print(result)
        
    def close(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

# main
dbname = 'example.db'
db = DB(dbname)
create_table_R = 'create table if not exists R(A char(1),B char(1),C char(1))'
create_table_S = 'create table if not exists S(B char(1),C char(1),D char(1))'
sql_insert = """insert into %s values(?,?,?)"""
r = [(2,4,6),(3,5,7),(7,4,6)]
s = [(5,7,3),(4,6,2),(5,7,9)]
# 打印R,S
print('[例]已知关系R,S如下，求R与S的自然连接。')
result = '\n'.join(map(repr, r)).replace('(','').replace(')','')
print(f'关系R\nA  B  C\n-------\n{result}\n')
result = '\n'.join(map(repr, s)).replace('(','').replace(')','')
print(f'关系S\nB  C  D\n-------\n{result}\n')

# 创建R，S
db.cur.execute(create_table_R)
db.cur.execute(create_table_S)

# 往表R,S插入元组
"""
for t in r:
    db.cur.execute(sql_insert % 'R', t)
for t in s:
    db.cur.execute(sql_insert % 'S', t)
""" 
# R,S作自然连接
print('R与S的自然连接结果为：')
sql_natural_join = 'select * from R natural join S'
db.cur.execute(sql_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'A  B  C  D\n----------\n{result}')