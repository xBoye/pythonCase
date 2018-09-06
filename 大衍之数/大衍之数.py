# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:00:09 2018
@title：大衍之数五十
@author: ff7f
@sqlite3数据库yi.db中表g64履卦开始有6,7条卦gname编码有问题。。
君子居则观其象而玩其辞，动则观其变而玩其占。
"""
import random
import sqlite3
import time
from g64dict import g64s    #64卦字典
from j4096dict import j4096s   #易林字典

shi_fa = "大衍之数五十，其用四十有九。分而为二以象两，挂一以象三，揲之以四以象四时，归奇于撝以象闰，五岁再闰，故再撝而后挂。"
print('\n> 大衍筮法', end='')   #, shi_fa, sep='\n')

#成爻设卦之步骤
#第一步：大衍之数五十，其用四十有九
Da_yan_shu = 50
Yong_shu = Da_yan_shu - 1

def bian(Yong_shu, n=1):
    #三变成爻
    #第二步：一变四营
    #所谓四营，就是分二、挂一、揲四、归奇四个环节。
    #第一营：分而为二以象两。
    liang_yi_1 = random.randint(1,Yong_shu-1)
    liang_yi_2 = Yong_shu - liang_yi_1
    #print(liang_yi_1, liang_yi_2)

    #第二营：挂一以象三。第一变挂一，之后不再挂一
    if n==1:
        liang_yi_1 -= 1   #挂一

    #第三营：揲之以四以象四时，归奇于扐以象闰。
    yu_shu_1 = liang_yi_1 % 4
    if yu_shu_1==0:
        yu_shu_1 = 4
    liang_yi_1 -= yu_shu_1

    #第四营：五岁再闰，故再扐而后挂。
    yu_shu_2 = liang_yi_2 % 4
    if yu_shu_2==0:
        yu_shu_2 = 4
    liang_yi_2 -= yu_shu_2

    #第1变结束
    #print(liang_yi_1, yu_shu_1)
    #print(liang_yi_2, yu_shu_2)
    
    Yong_shu = liang_yi_1+liang_yi_2
    logging('第%s变：%s' % (n, Yong_shu), end='   ')
    
    return Yong_shu

def gen_yao(Yong_shu):
    #三变成爻
    for n in range(1,4):
        Yong_shu = bian(Yong_shu,n)
    return int(Yong_shu/4)

def gen_gua(Yong_shu):
    #十八变成卦，每卦6爻
    yaos = []
    logging('> 机器卜筮助理 %s' % now().rjust(28))   #三变成爻，十八变成卦
    for y in range(1,6+1):
        yao_shu = gen_yao(Yong_shu)
        yaos.append(yao_shu)
        #print('第%s爻:' % y, yao_shu)
        #save('第%s爻：%s' % (y,yao_shu))
        logging('第%s爻：%s' % (y,yao_shu))
    yaos = yaos[::-1]
    ben_gua = [x%2 for x in yaos]
    gbin0 = ''.join(map(str,ben_gua))
    
    #变卦
    bian_gua = []
    for x in yaos:
        if x == 9:
            bian_gua.append(0)
        elif x==6:
            bian_gua.append(1)
        else:
            bian_gua.append(x%2)
    gbin1 = ''.join(map(str,bian_gua))
    
    yaos = repr(yaos)[1:-1].replace(', ','')
    #print(gbin0, gbin1, sep='\n')
    return gbin0, gbin1,yaos

def get_gname(gbin):
    '''读卦'''
    c = sqlite3.connect('yi.db')
    cur = c.cursor()
    sql = 'select gname from g64 where gbin = "%s"' % gbin
    cur.execute(sql)
    gname = cur.fetchone()[0]
    c.commit()
    c.close()
    return gname

def get_jci(jname):
    #读易林卦
    c = sqlite3.connect('yi.db')
    cur = c.cursor()
    sql = 'select jci from j4096 where jname = "%s"' % jname
    cur.execute(sql)
    jci = cur.fetchone()[0]
    c.commit()
    c.close()
    #print(jci)
    return jci

def save(msg, end='\n'):
    #保存筮例
    with open('筮例.log','a',encoding='utf8') as f:
        print(msg, file=f, end=end)
        
def logging(msg, end='\n', filename='筮例.log', addtime=False, outo='ALL'):
    # 保存实例，参数：
    # msg: 输出消息
    # end: 输出断行和同行接续
    # filename: 输出日志文件
    # addtime=True: 添加当前时间; False: 不添加时间
    # outo='ALL|STD|FILE': 同时输出到屏幕和日志； STD: 到屏幕； FILE: 日志文件
    
    if outo in ['ALL', 'STD']:
        if addtime:
            print(msg+'\n'+now(), end=end)
        else:
            print(msg, end=end)
    
    if outo in ['ALL', 'FILE']:
        with open(filename,'a',encoding='utf8') as f_log:
            if addtime:
                print(msg+'\n'+now(), file=f_log, end=end)
            else:
                print(msg, file=f_log, end=end)

def now():
    #当前日期时间
    _now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return _now

def 大衍筮法():
    #大衍筮法
    gbin0, gbin1, yaos = gen_gua(Yong_shu)
    ben_gua = g64s[gbin0]
    bian_gua = g64s[gbin1]
    #ben_gua = get_gname(gbin0)
    #bian_gua = get_gname(gbin1)

    logging('六爻(%s) >> 本卦-%s(%s) >> 变卦-%s(%s)' % (yaos, ben_gua, gbin0, bian_gua, gbin1))

    jname = ben_gua+'之'+bian_gua
    jci = j4096s[jname]         # 使用字典
    #jci = get_jci(jname)        # 使用数据库

    logging('[%s] %s' % (jname, jci))

#main
q = input('$ 请输入问题：')
while q:
    logging('\n$ 请输入问题：%s' % q, outo='FILE')
    大衍筮法()
    q = input('$ try again：')
