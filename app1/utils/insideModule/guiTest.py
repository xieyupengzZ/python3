#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: GUI编程
    在GUI中，每个Button、Label、输入框等，都是一个Widget
    Frame则是可以容纳其他Widget的Widget
    pack()方法把Widget加入到父容器中，并实现布局
    pack()是最简单的布局，grid()可以实现更复杂的布局
version: 1.0
Author: xieyupeng
Date: 2020-08-14 17:01:30
LastEditors: xieyupeng
LastEditTime: 2020-08-14 17:33:19
'''
from tkinter import Frame, Label, Button, Entry, messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    # def createWidgets(self):
    #     self.helloLabel = Label(self, text='Hello, world!')
    #     self.helloLabel.pack()
    #     self.quitButton = Button(self, text='Quit', command=self.quit)
    #     self.quitButton.pack()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()  # 放入容器
        self.alertButton = Button(self, text='Hello',
                                  command=self.hello)  # 按钮名称 和 触发十几分
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'  # 默认值 world
        messagebox.showinfo('Message', 'Hello, %s' % name)  # 信息弹窗


def gui1():
    app = Application()
    app.master.title('python is good')
    app.mainloop()


if __name__ == "__main__":
    gui1()