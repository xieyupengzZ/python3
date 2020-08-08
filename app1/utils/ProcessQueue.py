'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-07 23:44:35
LastEditors: xieyupeng
LastEditTime: 2020-08-08 18:52:46
'''
import multiprocessing
import time
from time import ctime


def consumer(input_q):
    print('consumer ', ctime())
    while True:
        item = input_q.get()
        print('consumer get ', item)
        input_q.task_done()  # JoinableQueue


def producer(sequeue, ouput_q):
    print('producer ', ctime())
    for item in sequeue:
        ouput_q.put(item)
        print('producer put ', item)


def main():

    jq = multiprocessing.JoinableQueue()

    ct = multiprocessing.Process(target=consumer, args=(jq, ))
    ct.daemon = True
    ct.start()

    sequeue = [1, 2, 3, 4, 5]
    producer(sequeue, jq)
    jq.join()  # JoinableQueue


'''
设置哨兵（随便设置一个值用来判断即可）
消费者根据哨兵退出
'''


def consumer2(input_q, name):
    print('consumer ', ctime())
    while True:
        item = input_q.get()
        if item is None:
            break
        print('%s get %s' % (name, item))
        time.sleep(1)
    print('consumer out')


def producer2(sequeue, ouput_q):
    print('producer ', ctime())
    for item in sequeue:
        ouput_q.put(item)
        print('producer put ', item)


def main2():

    q = multiprocessing.Queue()  # Queue

    ct = multiprocessing.Process(target=consumer2, args=(q, 'consumer1'))
    ct.start()
    ct2 = multiprocessing.Process(target=consumer2, args=(q, 'consumer2'))
    ct2.start()

    sequeue = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 22, 33, 44]
    producer(sequeue, q)
    # 设置哨兵，有几个进程设置几个，因为取出来就没了
    q.put(None)
    q.put(None)


if __name__ == '__main__':
    main()
    # main2()