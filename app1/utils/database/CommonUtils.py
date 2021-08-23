#!/usr/bin/python
# -*- encoding: utf-8 -*-
'常用方法' # 注解
__author__ = 'xieyupeng' # 作者
import tkinter
from datetime import datetime as dtime
from tkinter import messagebox
import re

# 弹窗信息
# tkinter的对话窗口必须要有一个主窗口，就像所有控件都需要放在一个窗口上
# 建立一个隐形窗口后就不会出现那个影响美观的自带窗口了
# messagebox 会引起阻塞，直到弹出框的被点击确定或关闭后
def showMsg(type,logfile,title,*msg):
    writelog(type,logfile,*msg)
    title = 'Python自动生成数据库脚本'
    printinfo = ''.join(msg)
    root = tkinter.Tk()
    root.withdraw()
    if type == 'info':
        messagebox.showinfo(title=title,message=printinfo)
    elif type == 'error':
        messagebox.showerror(title=title,message=printinfo)
    elif type == 'warn':
        messagebox.showwarning(title=title,message=printinfo)
    else:
        messagebox.showinfo(title=title,message=printinfo)

# 日志文件
def writelog(type,logfile,*msg):
    type = '【' + type.upper() + '】'
    nowtime = '【' + str(dtime.now()) + '】'
    log = nowtime + type + ''.join(msg) + '\n'
    print(log)
    with open(logfile,'a') as f:
        f.write(log)

# 查找字符串
# flags = re.I 不区分大小写
def searchStr(fromstr,str,flags):
    search = re.search(str, fromstr, flags=flags)
    index = -1
    if search is not None:
        index = search.span()[0]
    return index