#!/usr/bin/python
# -*- encoding: utf-8 -*-

import re
from calendar import month_abbr

# 简单文本替换
def replace1():
    text='mark,男,18,183'
    print(text)
    print(text.replace('18','19'))


# 正则表达式替换
def replace2():
    text = '今天是：11/28/2018'
    print(text)
    print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))


# 编译替换模式，可重复使用
def replace3():
    text = '今天是：11/28/2018'
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    print(text)
    print(datepat.sub(r'\3-\1-\2', text))


# 更复杂的情况，可使用回调函数
def replace4():
    text = '今天是：11/28/2018'
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    def change_date(m):
        mon_name = month_abbr[int(m.group(1))]
        return '{} {} {}'.format(m.group(3), mon_name, m.group(2))
    print(text)
    print(datepat.sub(change_date, text))


# 返回替换次数
def replace5():
    text = '今天是：11/28/2018,昨天是11/27/2018'
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    new_text, n = datepat.subn(r'\3-\1-\2', text)
    print(n)


if __name__ == '__main__':
    replace2()