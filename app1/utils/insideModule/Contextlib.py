#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 实现上下文，在方法调用前后，加上额外逻辑
version: 1.0
Author: xieyupeng
Date: 2020-08-10 14:21:29
LastEditors: xieyupeng
LastEditTime: 2020-08-11 18:02:19
'''
from contextlib import contextmanager
from contextlib import closing

'try...finally'


def openTest():
    try:
        f = open('text.txt', 'r')
        print(f.read())
    finally:
        if f:
            f.close()


'try...finally 的简写方式 with'


def withOpen():
    with open('text.txt', 'r') as f:
        print(f.read())


'''
1、
只要实现了__enter__和__exit__ 两个方法，称为实现了上下文，都可以使用 with 函数
enter（执行前），exit（执行后），效果就是：类中所有方法调用前后加上额外的逻辑
open 就是在调用后加上了文件关闭的逻辑
'''


class readContext():
    def __init__(self, name):
        self.name = name

    def __enter__(self):  # 执行前
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # 执行后
        if exc_type:
            print('error')
        else:
            print('exit')

    def get(self):
        return 'get name %s' % self.name

    def get2(self):
        return 'get name again %s' % self.name


def withTest():
    with readContext('zhangshou') as r:
        print(r.get())
        print(r.get2())


'''
2、@contextmanager（装饰器）也可以实现上下文，但是 @contextmanager 必须作用于一个 生成器
'''


class readContext2():
    def __init__(self, name):
        self.name = name

    def get(self):
        return 'get name %s' % self.name


'生成器作用于类'


@contextmanager
def readContextManage(name):
    print('enter')
    yield readContext2(name)
    print('exit')


def withTest2():
    with readContextManage('zhangshou') as r:
        r.get()


'生成器作用于方法'


@contextmanager
def sport():
    print('热身。。。')
    yield
    print('洗澡。。。')


def sportDetail():
    print('跑步中。。。')


def withTest3():
    with sport():
        sportDetail()  # 此处是你真正执行的代码


'''
@closing 可以为一个对象实现上下文，该对象必须实现 close() 方法
closing实现了__enter__ 和 __exit__ 方法，__exit__方法中调用了对象的close()方法
'''
class study():
    def __init__(self, name):
        self.name = name

    def close(self):
        print(self.name)


def withTest4():
    with closing(study('python')) as target:
        pass


if __name__ == '__main__':
    withTest4()