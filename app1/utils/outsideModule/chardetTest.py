'''
Descripttion: 字符编码
    bug记录：module 'chardet' has no attribute 'detect'
    原因：.py 文件名和功能模块重名了！！！！
version: 1.0
Author: xieyupeng
Date: 2020-08-14 16:03:10
LastEditors: xieyupeng
LastEditTime: 2020-08-14 16:17:50
'''
import chardet

# 检测输出 {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
# encoding 编码方式
# confidence 检测概率
# language 语言

def test1():
    print(chardet.detect(b'python is good'))
    gbkstr = '拍散'.encode('gbk')
    print(chardet.detect(gbkstr))
    utf8str = '谢宇鹏'.encode('utf-8')
    print(chardet.detect(utf8str))
    jpstr = '最新の主要ニュース'.encode('euc-jp')
    print(chardet.detect(jpstr))

if __name__ == "__main__":
    test1()