import threading
import asyncio
import sys
import LogTest
sys.path.append('/app1/utils')
'''
记录一个现象，获取日志器时：

1、都使用LogTest的属性logger，日志打印不会出现问题
2、都使用LogTest的方法logger1，出现问题：重复打印日志，因为会重复创建日志器（日志器名称是同一个）
3、一个使用方法logger1，一个使用方法logger2，并且两个方法中的日志器名称不同，日志打印不会出现问题

总结: 一个日志类，定义了一个方法，方法里创建一个日志器；
     如果引入该日志类，调用类中的方法获取日志器的时候，一旦重复调用了，不管是在一个方法里调用两次，还是在不同的方法里分别调用一次
     只要调用次数大于 1，就会导致同一个名称的日志器重复创建，日志就会重复输出
解决: 1 - 定义不同的方法，方法中的日志器名称不能相同，每个方法只能调用一次
     2 - 不使用方法，使用全局属性，重复获取该属性，不会导致日志器重复创建

这里是使用代码来实现日志器功能，比较简洁，好维护，缺点就是上面说的，太多调用方式，问题也多
很多项目还是用xml配置日志功能，就不存在代码那么多种调用方式，配置好了直接引用，问题较少，但是配置文件多了不好维护
'''


@asyncio.coroutine
def hello():
    logger = LogTest.logger1()
    # logger = LogTest.logger
    logger.debug('start....(%s)' % threading.currentThread())
    print('start....(%s)' % threading.currentThread())
    yield from asyncio.sleep(2)
    logger.debug('end....(%s)' % threading.currentThread())
    print('end....(%s)' % threading.currentThread())


@asyncio.coroutine
def hello1():
    logger = LogTest.logger1()
    # logger = LogTest.logger2()
    # logger = LogTest.logger
    logger.debug('start1....(%s)' % threading.currentThread())
    print('start1....(%s)' % threading.currentThread())
    yield from asyncio.sleep(2)
    logger.debug('end1....(%s)' % threading.currentThread())
    print('end1....(%s)' % threading.currentThread())


def main():
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello1()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
