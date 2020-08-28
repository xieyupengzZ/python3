'''
Descripttion:
3.4版本引入 asynico，异步操作在 coroutine 中通过 yield from 完成
执行了 yield from ，无需等待 yield from 返回，切换到另外一个任务继续执行；
等到 yield from 的返回通知后，再回来继续执行，全程都是一个线程，通过此机制，实现异步IO；
相比多线程，没有多线程切换的开销，没有多线程的锁机制，所以效率会高出很多；
一般用 多进程 + 协程 的方式开发
version: 1.0
Author: xieyupeng
Date: 2020-08-05 22:24:51
LastEditors: xieyupeng
LastEditTime: 2020-08-28 18:06:51
'''
import threading
import asyncio
from aiohttp import web

# 把一个生成器标记成 coroutine(协程)
@asyncio.coroutine  
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

# 获取不同官网 get请求的响应信息
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect  # 此处需要等待响应，会切换到另一个任务
    print('start get %s...' % host)
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()   # 刷新写缓冲区，如果需要等待，会切换到另一个任务，如果是瞬时完成的，就不会切换到另一任务，看数据量大小
    while True:
        print('start read %s...' % host)
        line = yield from reader.readline()  # 第一次执行此处，如果需要等待，会切换到另一个任务；等待完毕，切换回来时，就一直循环执行，直到全部读完退出才切换到另一个任务
        if line == b'\r\n':  # 请求头和请求体之间是有一个换行的
            print('------end read %s...' % host)
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


# 3.5版本引入async/await，用来简化 coroutine 的代码，async 替换 @asyncio.coroutine，await 替换 yield from
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


# aiohttp 是基于 asyncio 实现的HTTP框架，http就是一个io操作
async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))
    
# 下面的方法已经过时，请搜索最新 aiohttp用法
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

#  1、定义URL映射
routes = web.RouteTableDef()
@routes.get('/')
def index(request):
    return web.Response(body=b'<h1>Awesome App</h1>', content_type='text/html')

# 2、启动服务监听请求
def init():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    logging.info('server started at http://127.0.0.1:9000...')
    web.run_app(app, host='127.0.0.1', port=9000)

if __name__ == '__main__':
    # tasks1 = [hello(), hello()]
    # tasks2 = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    # tasks3 = [wget2(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    # main(tasks2)
    # main2()
    init()