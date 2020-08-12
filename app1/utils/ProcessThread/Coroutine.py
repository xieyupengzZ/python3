'''
Descripttion:
version: 1.0
Author: xieyupeng
Date: 2020-08-05 22:24:51
LastEditors: xieyupeng
LastEditTime: 2020-08-08 18:50:33
'''
import threading
import asyncio
from aiohttp import web
'''
3.4版本引入 asynico
异步操作在 coroutine 中通过 yield from 完成
执行了 yield from ，无需等待 yield from 返回，切换到另外一个任务继续执行，等到 yield from 的返回通知后，再回来继续执行。全程都是一个线程。
通过此机制，实现异步IO
'''


@asyncio.coroutine  # 把一个生成器标记成 coroutine(协程)
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())


@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect  # 此处会切换到另一个任务
    print('start get %s...' % host)
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()  # while中无法切换出去，只能一直执行到退出
        if line == b'\r\n':  # 请求头和请求体之间是有一个换行的
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


'''
3.5版本引入async/await，用来简化 coroutine 的代码，async 替换 @asyncio.coroutine，await 替换 yield from
'''


async def wget2(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect  # 此处会切换到另一个任务
    print('get connect %s...' % host)
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()  # while中无法切换出去，只能一直执行到退出
        if line == b'\r\n':  # 请求头和请求体之间是有一个换行的
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


def main(tasks):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(tasks))  # run_until_complete(运行_直到_结束)，阻塞直到协程运行结束
    loop.close()


'''
aiohttp 是基于 asyncio 实现的HTTP框架，http就是一个io操作
'''


async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')


async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv


def main2():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    # tasks1 = [hello(), hello()]
    # tasks2 = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    # tasks3 = [wget2(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    # main(tasks3)
    main2()