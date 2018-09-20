# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:55:24 2018
@title：P71-习题2.7
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
db= DB(dbname)
create_table_R = 'create table if not exists R(A char(1),B char(1))'
create_table_S = 'create table if not exists S(B char(1),C char(1))'
sql_insert = """insert into %s values(?,?)"""
r = [('a','b'),('c','b'),('d','e')]
s = [('b','c'),('c','a'),('b','d')]
# 打印R,S
print('[P71-习题2.7]已知关系R,S如下，求R与S的各种连接操作。')
result = '\n'.join(map(repr, r)).replace('(','').replace(')','').replace("'",'').replace(',',' ')
print(f'关系R\nA  B\n----\n{result}\n')
result = '\n'.join(map(repr, s)).replace('(','').replace(')','').replace("'",'').replace(',',' ')
print(f'关系S\nB  C\n----\n{result}\n')

# 创建R，S
db.cur.execute(create_table_R)
db.cur.execute(create_table_S)

# 往表R,S插入元组
for t in r:
    db.cur.execute(sql_insert % 'R', t)
for t in s:
    db.cur.execute(sql_insert % 'S', t)

# R,S作自然连接
print('[解答]\n>>> R与S的自然连接结果为：')
sql_natural_join = 'select * from R natural join S'   # 自然连接
db.cur.execute(sql_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'A  B  C\n-------\n{result}')

# θ连接
sql_xita_join = 'select * from R inner join S where R.B<S.C'  # θ连接
print('\n>>> R与S的θ连接(B<C)结果为：')
#result = '\n'.join(map(repr, db.cur.fetchall()))
result = db.select(sql_xita_join)
import re
result = re.sub("\(|\)|\'",'', result).replace(',','  ')
print(f'A  R.B S.B  C\n-------------\n{result}')

sql_xita_join = 'select * from R inner join S where R.A=S.C'  # θ连接
print('\n>>> R与S的θ连接(A=C)[等价于σA=C(R×S)]结果为：')
#result = '\n'.join(map(repr, db.cur.fetchall()))
result = db.select(sql_xita_join)
import re
result = re.sub("\(|\)|\'",'', result).replace(',','  ')
print(f'A  R.B S.B  C\n-------------\n{result}')

# R,S半连接（R,S自然连接结果在R属性上投影）
print('\n>>> R与S半连接(R,S自然连接结果在R属性上投影)结果为：')
sql_natural_join = 'select distinct R.A,R.B from R natural join S'   # 自然连接
db.cur.execute(sql_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'A  B\n----\n{result}')

# S,R半连接（S,R自然连接结果在R属性上投影）
print('\n>>> S与R半连接(S,R自然连接结果在关系S属性上投影)结果为：')
sql_natural_join = 'select distinct S.B,S.C from S natural join R'   # 自然连接
db.cur.execute(sql_natural_join)
result = '\n'.join(map(repr, db.cur.fetchall()))
import re
result = re.sub("\(|\)|\'",'', result).replace(',',' ')
print(f'B  C\n----\n{result}')

db.close()