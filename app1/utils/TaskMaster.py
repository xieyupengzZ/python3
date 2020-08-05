'''
1. Windows下在注册任务队列和结果队列时不支持lambda表达式，需要使用函数代替
2. 在绑定网络地址时不能为空，可以使用'127.0.0.1'代替空置
'''
import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()                                  # 发送任务的队列
result_queue = queue.Queue()                                # 接收结果的队列

class QueueManager(BaseManager):
    pass

def getTaskQueue():
    return task_queue

def getResultQueue():
    return result_queue

def doTaskMater():
    # QueueManager.register('get_task_queue', callable=lambda: task_queue)          # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    # QueueManager.register('get_result_queue', callable=lambda: result_queue)
    QueueManager.register('get_task_queue', callable=getTaskQueue)
    QueueManager.register('get_result_queue', callable=getResultQueue)
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')              # 绑定端口5000, 设置验证码'abc':
    manager.start()                                                                  # 启动Queue:

    task = manager.get_task_queue()                                                  # 获得通过网络访问的Queue对象:
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    print('Try get results...')

    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)

    manager.shutdown()
    print('master exit.')

if __name__ == '__main__':
    doTaskMater()
