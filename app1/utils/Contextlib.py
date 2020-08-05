from contextlib import contextmanager

'''
try...finally
'''
def openTest():
    try:
        f = open('text.txt', 'r')
        print(f.read())
    finally:
        if f:
            f.close()

'''
try...finally 的简写方式 with
'''
def withOpen():
    with open('text.txt', 'r') as f:
        print(f.read())

'''
只要实现了__enter__和__exit__ 两个方法，都可以使用 with 函数
enter（执行前），exit（执行后），相当于类中所有方法调用前后加上额外的逻辑
open 就是在调用后加上了文件关闭的逻辑
'''
class readContext():
    def __init__(self,name):
        self.name = name
    def __enter__(self):                            # 执行前
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
__enter__和__exit__ 的简写方式 @contextmanager（装饰器）
__enter__和__exit__ 只能在类中实现，如果使用 @contextmanager，还可以针对方法，使得调用某个方法前后，执行额外的逻辑
@contextmanager 必须作用有一个 生成器
'''
class readContext2():
    def __init__(self,name):
        self.name = name
    def get(self):
        return 'get name %s' % self.name

@contextmanager
def readContextManage(name):
    print('enter')
    q = readContext2(name)
    yield q
    print('exit')

def withTest2():
    with readContextManage('zhangshou') as r:
        r.get()

'''
@contextmanager 作用于方法
'''
@contextmanager
def sport():                            # 额外逻辑
    print('热身。。。')
    yield
    print('洗澡。。。')

def withTest3():
    with sport():
        print('跑步中。。。')             # 此处是你真正执行的代码

if __name__ == '__main__':
    withTest3()