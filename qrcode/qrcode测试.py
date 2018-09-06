# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 03:55:23 2018
@title：qrcode测试
@author: ff7f
"""
from myqrcode import QrCode, showimage
import webbrowser as web # 调用浏览器

# 调用默认浏览器打开url  
def browser(url):  
    web.open_new_tab(url)  

def test_url_qrcode(url, qrcodename, logo, boxsize=8):
    # 生成url qrcode测试
    
    #text = 'https://github.com/xBoye/pythonCase'
    #logo = 'github_logo.jpg'
    #qrcodename = 'githubqrcode.png'
    qc = QrCode()
    qc.createqrcode(url, qrcodename, logo, boxsize=boxsize)
    showimage(qrcodename)

    # 读qrcode
    url = qc.readqrcode(qrcodename)
    print(f'> url = {url}')

    if 'http' in url.lower():   # 是网址随后打开
        browser(url)


def test_han_qrcode():
    # 生成base64格式中文qrcode测试
    text = '《劝学文》[宋]赵恒\n富家不用买良田，书中自有千钟粟。\n安居不用架高楼，书中自有黄金屋。\n娶妻莫恨无良媒，书中自有颜如玉。\n出门莫恨无人随，书中车马多如簇。\n男儿欲遂平生志，六经勤向窗前读。'
    logo = '劝学logo.png'
    qrcodename = '劝学qrcode.png'
    qc = QrCode()
    qc.createqrcode(text, qrcodename, logo, boxsize=3, isbase64=True)
    showimage(qrcodename)
    
    # 读qrcode
    text = qc.readqrcode(qrcodename, isbase64=True)
    print(f'> 读出文本\n{text}')

def test_read_qrcode(qrcodename, isbase64=False):
    # 读qrcode图形，中文isbase64=True
    showimage(qrcodename)

    print('> 测试读二维码文本')
    qc = QrCode()
    text = qc.readqrcode(qrcodename, isbase64=isbase64)
    print(text)
    
 
if __name__ == '__main__':
    # 测试读二维码
    qrcodename = '坤qrcode.png'
    test_read_qrcode(qrcodename, isbase64=True)
    
    # 测试生成中文二维码
    #print('\n> 测试生成中文二维码')
    #test_han_qrcode()
    
    # 测试url二维码
    url ='http://gupuyuan2015.blog.163.com/blog/static/2467651072008626840486/'
    logo = '缘logo.png'
    qrcodename = '博文1qrcode.png'
    print('\n> 测试url二维码')
    test_url_qrcode(url, qrcodename, logo)