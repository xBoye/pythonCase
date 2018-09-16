# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 14:10:36 2018
@title：读Excel数据
@author: ff7f
"""
import xlrd
test = 1
if test:
    xlsfile = "test.xls"
else:
    xlsfile = "records.xls"
book = xlrd.open_workbook(xlsfile)
for sheet in book.sheets():
    print(f'>>> 工作表名：{sheet.name}')
sheet = book.sheet_by_index(0)
print(f'>>> 解析Excel工作表({sheet.name})数据...')
students = []
for i in range(sheet.nrows):
    row = sheet.row_values(i)[1:]
    if i==1:
        classtime = row[2]
    elif i==2:
        classplace = row[2]
    elif i==3:
        cno, cnum = row[2].split('-')
        cname, tname = row[10], row[23]
        
    elif i in [4,5]:
        continue
    elif i >= 6:
        row[0], row[1] = int(row[0]), int(row[1])
        students.append((row[1],row[2],row[3]))
    print(i, end=' ')
    for n,cell in enumerate(row):
        if cell:
            print(cell, end=' ')
    print('')

# 解析基本数据data=(上课时间,上课地点,课号,课序号,课程名,上课教师,上课班级)
sclass = row[3]
data = (classtime, classplace, cno, cnum, cname, tname, sclass)

import sqlite3
import os
def parse_excel():
    # 创建数据库，解析Excel电子表格数据
    dbname = 'student.db'
    if os.path.exists(dbname):
        os.remove(dbname)
    # 创建教师表t
    create_table_teacher = """
        create table if not exists t(     
            tno     char(10) primary key,
            tname   char(10),
            title   char(10))"""
         
    # 创建学生表s
    create_table_student = """
        create table if not exists s(
            sno     char(10) primary key,
            sname   char(10),
            age     smallint,
            sex     char(2),
            sclass  char(10))"""
        
    # 创建课程表c
    create_table_course = """
        create table if not exists c(
            cno        char(10) primary key,
            cname      char(20),
            class_hour smallint
            )"""
    
    # 创建授课表sh(schedules)
    create_table_schedules = """
        create table if not exists sh(
            tno        char(10),
            tname      char(10),
            cno        char(10),
            cnum       char(5),
            classtime  text,
            classplace text,
            sclass     char(10)
            )"""

    # 创建选课表sc
    create_table_sc = """
        create table if not exists sc(
            sno   char(10),
            cno   char(10),
            score smallint)"""
    
    # 创建记录表rec(records)
    create_table_records = """
        create table if not exists rec(
            sno    char(10) primary key,
            cno    char(10),
            cnum   char(5),
            cdate  date,
            state  char(1)
            )"""
    
    # 查询创建的表
    select_tables = """select name from sqlite_master where type='table'"""
    
    # 插入数据
    insert_student = """insert into s(sno,sname,sclass) values(?,?,?)"""
    insert_schedules = """insert into sh(tname,cno,cnum,classtime,classplace,sclass) values(?,?,?,?,?,?)"""
    insert_teacher = """insert into t(tno,tname) values(?,?)"""
    insert_course = """insert into c(cno,cname) values(?,?)"""
    
    # 查询插入的数据
    select_course = """select * from c"""   # 查询课程
    select_teacher = """select * from t"""  # 查询教师
    select_student = """select * from s"""  # 查询学生
    
    # 创建数据库
    try:
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        # 创建表
        cur.execute(create_table_teacher)
        cur.execute(create_table_student)
        cur.execute(create_table_course)
        cur.execute(create_table_schedules)
        cur.execute(create_table_sc)
        cur.execute(create_table_records)
        
        # 查询已创建的表
        cur.execute(select_tables)
        tables = []
        for table in cur.fetchall():
            tables.append(table[0])
        print(f'>>> 确认已经创建的表：{tables}')
        print('#教师表t, 学生表s, 课程表c, 授课表sh, 选课表sc, 教学记录表rec')
        
        # 插入数据
        print('>>> 插入解析数据..')
        cur.execute(insert_course,(cno, cname))    # 插入课程
        cur.execute(insert_teacher,('t1',tname))   # 插入教师
        for s in students:                         # 插入学生 
            cur.execute(insert_student, s)
        
        # 查询课程
        print('>>> 查询数据..')
        cur.execute(select_course)
        courses = cur.fetchall()
        print(f'>>> 课程记录：{courses}')
        
        #查询教师
        cur.execute(select_teacher)
        teachers = cur.fetchall()
        print(f'>>> 教师记录：{teachers}')
        
        # 查询学生
        cur.execute(select_student)
        sel_students = cur.fetchall()
        print(f'>>> 学生记录\n{sel_students}')
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.commit()
        con.close()
        
# main 
parse_excel()