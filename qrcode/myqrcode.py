# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:05:58 2018
@title: 使用qrcode生成二维码
@author: ff7f
"""
from PIL import Image
import qrcode
import zxing
import base64
import webbrowser as web # 调用浏览器
import matplotlib.image as mpimg #image 用于读取图片
import matplotlib.pyplot as plt

class QrCode:
    
    def __init__(self):
        
        self.qrtext = None
        self.qrtext_base64 = None
        self.qrcodename = None
        self.qrlogo = None
        self.isbase64 = False
        self.qrdata = None
        

    def createqrcode(self, text=None, qrcodename=None, logo=None, boxsize=4, isbase64=False):
        """ create qrcode
        parameters:
            text: 文本
            qrcodename: 输入二维码图形文件
            logo: 嵌入logo
            boxsize: 控制二维码中每个小格子包含的像素数，默认为10
            isbase64: 文本是否base64编码，中文文本为True
        """
        
        self.qrtext = text
        self.qrcodename = qrcodename
        self.qrlogo = logo
        self.isbase64 = isbase64
        if isbase64:
            text = han2base64(text.replace(' ', '　'))
            self.qrtext_base64 = text
            
        if logo:
            create_logo_qrcode(text, qrcodename, logo, boxsize)
        else:
            create_qrcode(text, qrcodename, boxsize)
    
    
    def readqrcode(self, qrcodename, isbase64=False):
        # read qrcodeimg
        
        self.qrdata = reg_qrcode(qrcodename)
        self.qrtext = self.qrdata.parsed
        if isbase64:
            self.qrtext_base64 = self.qrtext
            self.qrtext = base642han(self.qrtext)
        return self.qrtext

def create_qrcode(text=None, qrcodename=None, boxsize=4):
    qr = qrcode.QRCode(
        version=1,  # 值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
        error_correction=qrcode.ERROR_CORRECT_H, # 用于控制二维码的错误纠正程度
        box_size=boxsize, # 控制二维码中每个小格子包含的像素数，默认为10
        border=4, # 二维码四周留白，包含的格子数，默认为4
        #image_factory=None,  保存在模块根目录的image文件夹下
        #mask_pattern=None
    )
 
    qr.add_data(text) # QRCode.add_data(data)函数添加数据
    qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片
    img = qr.make_image()
    img.save(qrcodename, quality=100)
    #img.show()


def create_logo_qrcode(text=None, qrcodename=None, logoname=None, boxsize=4):
    qr = qrcode.QRCode(
        version=1,  # 值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
        error_correction=qrcode.ERROR_CORRECT_H, # 用于控制二维码的错误纠正程度
        box_size=boxsize, # 控制二维码中每个小格子包含的像素数，默认为10
        border=4, # 二维码四周留白，包含的格子数，默认为4
        #image_factory=None,  保存在模块根目录的image文件夹下
        #mask_pattern=None
    )
 
    qr.add_data(text) # QRCode.add_data(data)函数添加数据
    qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片
 
    img = qr.make_image()
    img = img.convert("RGBA") # 二维码设为彩色
    logo = Image.open(logoname) # 传gif生成的二维码也是没有动态效果的
 
    w , h = img.size
    logo_w , logo_h = logo.size
    factor = 4   # 默认logo最大设为图片的四分之一
    s_w = int(w / factor)
    s_h = int(h / factor)
    if logo_w > s_w or logo_h > s_h:
        logo_w = s_w
        logo_h = s_h
 
    logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
    l_w = int((w - logo_w) / 2)
    l_h = int((h - logo_h) / 2)
    logo = logo.convert("RGBA")
    img.paste(logo, (l_w, l_h), logo)
    #save_name = os.getcwd()+'\' + qrcodename
    img.save(qrcodename, quality=100)
    #img.show()


def reg_qrcode(qr_img):
    # 识别二维码
    zx = zxing.BarCodeReader()
    data = zx.decode(qr_img)
    
    return data     # data.parsed

def han2base64(text):
    #汉字转为base64
    text_byte = text.encode()
    text_b64 = base64.b64encode(text_byte)
    
    return text_b64

def base642han(text_b64):
    # base64编码还原汉字
    text_byte = base64.b64decode(text_b64)
    
    return text_byte.decode()

def load(textfile):
    # 导入文本信息
    with open(textfile, encoding='utf8') as f:
        text = f.read()
    return text


def showimage(imagename, size=(7,7)):
    # 显示图形
    img = mpimg.imread(imagename)      # 读取图片文件
    plt.figure(figsize=size)
    plt.imshow(img)      
    plt.axis('off')            
    plt.show()


# 调用默认浏览器打开url  
def browser(url):  
    web.open_new_tab(url)  


def test1():
    # 使用QrCode类测试案例
    text = load('坤.txt')          # 文本
    #print(text)
    qrcodename = '坤qrcode.png'    # 二维码图片
    logo = '坤logo.png'           # 嵌入logo
    qr = QrCode()                  # qrcode类
    # create qrcode
    print('> 生成二维码。。')
    qr.createqrcode(text,qrcodename,logo,boxsize=3, isbase64=True)
    showimage(qrcodename, (6,6))
    
    # read qrcode
    print('> 读取二维码。。')
    text = qr.readqrcode(qrcodename, isbase64=True)
    print(text)


def test2():
    # 直接用函数生成二维码
    text = '《苔》袁枚 白日不到处，青春恰来时。苔花如米小，也学牡丹开。'
    print(f'> 文本信息\n{text}')
    text = han2base64(text)     # 汉字转为base64
    logo = '苔logo.png'
    qrcodename = '苔qrcode.png'
    #生成二维码
    print('> 生成二维码。。')
    create_logo_qrcode(text,qrcodename,logo, boxsize=4)
    showimage(qrcodename)
    
    #识别二维码
    print('> 读取二维码。。') 
    data = reg_qrcode(qrcodename)
    text = base642han(data.parsed)
    print(text)


if __name__ == '__main__':
    test1()   #使用QrCode类
    test2()   #使用函数

"""
import qrcode 
qr = qrcode.QRCode(     
    version=1,     
    error_correction=qrcode.constants.ERROR_CORRECT_L,     
    box_size=10,     
    border=4, 
) 
qr.add_data('hello, qrcode') 
qr.make(fit=True)  
img = qr.make_image()
img.save('test.png')
"""