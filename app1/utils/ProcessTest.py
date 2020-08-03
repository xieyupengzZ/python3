'''
多进程
'''
import multiprocessing
from time import ctime,sleep
import os

'''
第一种创建方法
multiprocessing.Process(target,args)
默认非守护进程，父进程结束，不影响子进程
'''
def process1():
    while True:
        print( 'this time is ',ctime())
        sleep(1)

def main1():
    p = multiprocessing.Process(target=process1)
    p.start()
    while True:
        print( 'TIME:',ctime())
        sleep(5)

'''
第二种方法
派生子类
'''
class childProcess(multiprocessing.Process):

    def __init__(self,seconds):
        super().__init__()
        self.seconds = seconds

    def run(self):
        while True:
            print( 'this time is ',ctime())
            sleep(self.seconds)

def main2():
    c = childProcess(1)
    c.start()
    while True:
        print( 'TIME:',ctime())
        sleep(5)

'''
os中查看父进程和子进程
'''

def info():
    print('parent id: ',os.getppid())
    print('child id: ',os.getpid())

def printInfo():
    info()

def main3():
    info()
    t = multiprocessing.Process(target=printInfo())
    t.start()

if __name__ == '__main__':
    # main1()
    # main2()
    main3()


