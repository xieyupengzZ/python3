'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-09-02 22:19:08
LastEditors: xieyupeng
LastEditTime: 2020-09-02 22:31:47
'''
from PIL import Image

im = Image.open('1.jpg')
im.resize((128,128))
im.save('1.ico', 'ico')