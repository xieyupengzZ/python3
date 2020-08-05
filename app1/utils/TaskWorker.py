import time, sys, queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')                         # 从网络上获取Queue，所以注册时只提供名字
QueueManager.register('get_result_queue')

server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
manager = QueueManager(address=(server_addr, 5000), authkey=b'abc')   # 地址，端口和验证码注意保持与task_master.py设置的完全一致
manager.connect()                                                     # 从网络连接
task = manager.get_task_queue()                                       # 获取Queue的对象
result = manager.get_result_queue()

for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty.')

print('worker exit.')