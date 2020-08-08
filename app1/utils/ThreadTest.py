'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-01 18:55:27
LastEditors: xieyupeng
LastEditTime: 2020-08-08 18:54:37
'''
import time
import _thread as thread
import threading


def loop1(name):
    print(name, ' start time:', time.ctime())
    time.sleep(4)
    print(name, ' end time:', time.ctime())


def loop2(name1, name2):
    time.sleep(1)
    print(name1, name2, 'loop2 start time:', time.ctime())
    time.sleep(2)
    print(name1, name2, 'loop2 end time:', time.ctime())


# 第一种方法
# thread.start_new_thread 启动一个新线程，默认是守护线程
# 第一个参数是函数，第二个参数是函数的参数
# 注意，第二个参数必须是元组，所以如果参数只有一个，必须在参数后面加逗号
def main():
    thread.start_new_thread(loop1, ('xieyupeng', ))
    thread.start_new_thread(loop2, ('xieyupeng', 'zhangzhao'))
    time.sleep(2)
    print('main end time', time.ctime())


# 第二种方法
# threading.Thread 启动一个新线程，默认是非守护线程
# join 会等待线程结束再继续执行
def main2():
    t1 = threading.Thread(target=loop1, args=('xieyupeng', ))
    # t1.setDaemon(True) # 设置成守护线程
    t1.start()
    t2 = threading.Thread(target=loop2, args=('xieyupeng', 'zhangzhao'))
    # t2.setDaemon(True)
    t2.start()
    # t1.join()
    # t2.join()
    time.sleep(2)
    print('main2 end time', time.ctime())


def loop():
    print('start time:', time.ctime())
    time.sleep(3)


def main3():
    t1 = threading.Thread(target=loop, args=())
    t1.setName('thread1')
    t1.start()
    t2 = threading.Thread(target=loop, args=())
    t2.setName('thread2')
    t2.start()
    t3 = threading.Thread(target=loop, args=())
    t3.setName('thread3')
    t3.start()
    time.sleep(1)
    print('thread count:', threading.activeCount())
    for thr in threading.enumerate():
        print('runing:', thr.getName())


if __name__ == '__main__':
    '''
    1
    main()不用等待线程执行完，就先执行完了；mian()执行完，程序就要退出了；
    thread.start_new_thread 默认创建的是守护线程，主线程退出，它们也会结束
    所以如果想要看线程睡眠后继续执行，必须要等待，不能退出
    '''
    # main()
    # time.sleep(6)
    '''
    2 join本身会等待线程执行完毕再继续执行，替代了1方案
    '''
    main2()
    '''
    3 线程常用属性
    '''
    # main3()