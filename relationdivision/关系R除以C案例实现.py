# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 23:27:33 2018
@title: 关系R除以C案例代码验证
@author: ff7f
[P48例2.5]已知关系R、C，求R÷C。
关系R
sno,sname,cno,cname
s1,bao,c1,DB
s1,bao,c2,OS
s1,bao,c3,DS
s1,bao,c4,MIS
s2,gu,c1,DB
s2,gu,c2,OS
s3,an,c2,OS
s4,li,c2,OS
s4,li,c4,MIS

关系C
cno, cname
c2,OS
c4,MIS

关系R÷C计算结果：
sno,sname
s1,bao
s4,li
"""
from db import DB
import os

q = "\n[关系除法问题 P48例2.5]\n已知关系R、C，求R÷C。"
print(q)

dbname = 'temp.db'
if os.path.exists(dbname):
    os.remove(dbname)

create_table_R = """create table R(
                       sno   char(4),
                       sname char(10),
                       cno   char(4),
                       cname char(20))"""

create_table_C = """create table %s(
                       cno   char(4),
                       cname char(20))"""
# 插入数据SQL
sql_insert_R = "insert into R values(?,?,?,?)"
sql_insert_C = "insert into %s values(?,?)"

# 创建并连接数据库
db = DB(dbname)
# 创建关系R
db.cur.execute(create_table_R)

# 插入关系R元组
r = [('s1','bao','c1','DB'),('s1','bao','c2','OS'),
     ('s1','bao','c3','DS'),('s1','bao','c4','MIS'),
     ('s2','gu','c1','DB'),('s2','gu','c2','OS'),
     ('s3','an','c2','OS'),('s4','li','c2','OS'),
     ('s4','li','c4','MIS')]

for t in r:
    db.insert(sql_insert_R, '',t)

# 查询数据
sql_select_R = "select * from R"
result = db.select(sql_select_R)
print(f'>>> 关系R\nsno  sname  cno  cname\n----------------------\n{result}')

# 关系R÷C实现
X = ['C1','C2','C3']
x = [[('c2','OS')],[('c2','OS'),('c4','MIS')],[('c1','DB'),('c2','OS'),('c4','MIS')]]

# 查询关系C SQL语句
sql_select_C = "select * from %s"

# 用SQL-select语句验证关系R÷C
sql_result = """
select distinct sno, sname
from R as X 
where not exists( 
    select * from %s as C 
    where not exists( 
        select * from R as Y 
        where Y.sno=X.sno and Y.cno=C.cno))"""

for C, c in zip(X, x):
    # 创建关系C
    db.cur.execute(create_table_C % C)
    # 插入关系C元组
    for t in c:
        db.insert(sql_insert_C, C, t)

    # 查询关系C
    result = db.select(sql_select_C, C)
    print(f'\n>>> 关系{C}\ncno  cname\n----------\n{result}')

    result = db.select(sql_result, C)
    print(f'\n>>> 关系R÷{C}\nsno  sname\n----------\n{result}')

db.close()