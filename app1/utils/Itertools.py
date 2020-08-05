import itertools
import time
'''
itertools 提供了用户操作迭代对象的函数

无限迭代（只在for循环中生效）：
count(n)，从 n 开始，无限往下
cycle(s)，循环迭代 s 对象
repeat(s,n)，把 s 迭代 n 次

takewhile()：截取有限序列，如果截取的是无限序列，则返回空
chain()：合并一组迭代对象，类似ChainMap()
groupby()：相邻重复元素放到同一个集合中（默认区分大小写），还可以加一个处理函数
'''

def count():
    c = itertools.count(10)
    for i in c:
        print(i)
        time.sleep(1)

def cycle():
    c = itertools.cycle('xyp')
    for i in c:
        print(i)
        time.sleep(1)

def repeat():
    r = itertools.repeat('xyp',10)
    for i in r:
        print(i)
        time.sleep(1)

def check(x):
    return x <= 10

def takewhile():
    c = itertools.count(1)
    ns = itertools.takewhile(lambda x : x <= 10,c)
    print(list(ns))

def chain():
    c = itertools.chain('xieyupeng','zhangpang','python')
    for i in c:
        print(i)

def groupby():
    print('区分大小写：')
    g = itertools.groupby('AaPPAzZZ')                               # 默认区分大小写
    for key,group in g:
        print(key,list(group))
    print('忽略大小写：')
    g2 = itertools.groupby('AaPPAzZZ',lambda x : x.upper())         # 加一个处理函数，大写后再比较
    for key,group in g2:
        print(key,list(group))

if __name__ == '__main__':
    # count()
    # cycle()
    # repeat()
    # takewhile()
    # chain()
    groupby()