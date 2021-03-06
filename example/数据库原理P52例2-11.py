# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:55:24 2018
@title：examples
@author: ff7f
"""
import sqlite3
import os
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
if os.path.exists(dbname):
    os.remove(dbname)
db = DB(dbname)
create_table_R = 'create table if not exists R(A char(1),B char(1),C char(1))'
create_table_S = 'create table if not exists S(B char(1),C char(1),D char(1))'
sql_insert = """insert into %s values(?,?,?)"""
r = [('a','b','c'),('b','b','f'),('c','a','d')]
s = [('b','c','d'),('b','c','e'),('a','d','b'),('e','f','g')]
# 打印R,S
print('[例]已知关系R,S如下，求R与S的自然连接(P52-例2.11)。\n[注]sqlite3数据库到目前为止只支持左外连接，不支持右外连接和完全外连接。')
result = '\n'.join(map(repr, r)).replace('(','').replace(')','').replace("'",'')
print(f'关系R\nA  B  C\n-------\n{result}\n')
result = '\n'.join(map(repr, s)).replace('(','').replace(')','').replace("'",'')
print(f'关系S\nB  C  D\n-------\n{result}\n')

# 创建R，S
db.cur.execute(create_table_R)
db.cur.execute(create_table_S)

# 往表R,S插入元组
for t in r:
    db.cur.execute(sql_insert % 'R', t)
for t in s:
    db.cur.execute(sql_insert % 'S', t)
 
# R,S作自然连接
sql_natural_join = """select * from R natural join S"""            # 自然连接
sql_left_outer_natural_join = """select * from R left outer natural join S"""      # 自然左外连接
sql_left_outer_natural_join2 = """select * from S left outer natural join R"""

print('R与S的自然连接结果为：')
db.cur.execute(sql_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'A  B  C  D\n----------\n{result}')


print('\nR与S的自然左外连接结果为：')
db.cur.execute(sql_left_outer_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'A  B  C  D\n----------\n{result}')

print('\nS与R的自然左外连接结果为：')
db.cur.execute(sql_left_outer_natural_join2)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'B  C  D  A\n----------\n{result}')


db.close()