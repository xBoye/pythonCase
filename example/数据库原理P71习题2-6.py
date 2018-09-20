# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:55:24 2018
@title：数据库原理P71习题2.6
@author: ff7f
"""
import sqlite3
import os
import re

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
        result = re.sub("\(|\)|\'",'', result).replace(',','  ')
        #print(result)
        return result
        
    def close(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

# main
dbname = 'example.db'
if os.path.exists(dbname):
    os.remove(dbname)
db = DB(dbname)
create_table_R = 'create table if not exists R(A int(1),B int(1),C int(1))'
create_table_S = 'create table if not exists S(A int(1),B int(1),C int(1))'
sql_insert = """insert into %s values(?,?,?)"""
r = [(3,6,7),(2,5,7),(7,2,3),(4,4,3)]
s = [(3,4,5),(7,2,3)]
# 打印R,S
print('[P71-习题2.6]已知关系R,S如下，求R与S的集合运算和关系运算。')
result = '\n'.join(map(repr, r)).replace('(','').replace(')','').replace("'",'').replace(',',' ')
print(f'关系R\nA  B  C\n-------\n{result}\n')
result = '\n'.join(map(repr, s)).replace('(','').replace(')','').replace("'",'').replace(',',' ')
print(f'关系S\nB  C  D\n-------\n{result}')

# 创建R，S
db.cur.execute(create_table_R)
db.cur.execute(create_table_S)

# 往表R,S插入元组
for t in r:
    db.cur.execute(sql_insert % 'R', t)
for t in s:
    db.cur.execute(sql_insert % 'S', t)

# 关系的集合运算
r = set(r)
s = set(s)
print('\n[解答]\n>>> R∪S结果为：')
result = '\n'.join(map(repr, r|s)).replace('(','').replace(')','').replace(',',' ')
print(f'A  B  C\n-------\n{result}')

print('\n>>> R-S结果为：')
result = '\n'.join(map(repr, r-s)).replace('(','').replace(')','').replace(',',' ')
print(f'A  B  C\n-------\n{result}')

print('\n>>> R∩S结果为：')
result = '\n'.join(map(repr, r&s)).replace('(','').replace(')','').replace(',',' ')
print(f'A  B  C\n-------\n{result}')

# 笛卡尔积R×S
sql_xita_join = 'select * from R inner join S'  # 笛卡尔积
print('\n>>> R与S笛卡尔积结果为：')
result = db.select(sql_xita_join)
print(f'R.A R.B R.C S.A S.B S.C\n-----------------------\n{result}')

# 投影
sql_select = "select C,B from S"
print('\n>>> 投影π3,2(S)结果为：')
result = db.select(sql_select)
print(f'C   B\n-----\n{result}')

# 选择
sql_select = "select * from R where B<5"
print('\n>>> 选择σB<5(R)结果为：')
result = db.select(sql_select)
print(f'A   B   C\n---------\n{result}')

# θ连接
sql_xita_join = 'select * from R inner join S where R.B<S.B'  # θ连接
print('\n>>> R与S的θ连接(B<B)结果为：')
result = db.select(sql_xita_join)
print(f'R.A R.B R.C S.A S.B S.C\n-----------------------\n{result}')

# R,S作自然连接
sql_natural_join = "select * from R natural join S"   # 自然连接
print('\n>>> R与S的自然连接结果为：')
result = db.select(sql_natural_join)
print(f'A   B   C\n---------\n{result}')

db.close()