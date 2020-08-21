#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: TCP编程，建立可靠连接
HTTP：必须客户端先给服务端发，服务端才给客户端回；所以是一来一回作为一个批次；
TCP：全双工，双方都可以向对方发送数据，先后次序根据TCP协议
version: 1.0
Author: xieyupeng
Date: 2020-08-17 10:03:10
LastEditors: xieyupeng
LastEditTime: 2020-08-20 16:15:18
'''

import socket
import time
import threading
import multiprocessing


def clientSocket():
    # 创建一个客户端socket:
    # AF_INET：IPv4，AF_INEF6：IPv6
    # SOCK_STREAM：TCP协议
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('www.sina.com.cn', 80))
    # 发送数据:
    # Connection:close 表示本次TCP连接在请求处理完后会关闭
    s.send(
        b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n'
    )
    # 接收数据:
    buffer = []
    while True:
        # 每次最多接收1k字节:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    # 关闭连接:
    s.close()

    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))
    # 把接收的数据写入文件:
    with open('sina.html', 'wb') as f:
        f.write(html)


def localServer():
    # 创建服务端
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('127.0.0.1', 9999))
    # 监听端口：
    s.listen()
    print('开始监听端口...')
    while True:
        # 接受一个新连接（会阻塞，没接受到就一直等待）:
        sock, addr = s.accept()
        time.sleep(1)
        print('监听到端口有新的连接请求，开启新线程处理')
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


def tcplink(sock, addr):
    print('server:Accept new connection from %s:%s...' % addr)
    while True:
        # 接收消息(会阻塞，没收到就一直等待):
        data = sock.recv(1024)
        if not data or data.decode('utf-8') == 'exit':
            break
        print('server get：', data)
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('server:Connection from %s:%s closed.' % addr)


def localClient():
    time.sleep(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('127.0.0.1', 9999))
    for data in [b'Michael', b'Tracy', b'Sarah']:
        # 发送数据:
        print('client send ', data)
        s.send(data)
        time.sleep(1)
        # 接收消息(会阻塞，没收到就一直等待):
        print('client get:', s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    s.close()


if __name__ == "__main__":

    client = multiprocessing.Process(target=localClient)
    server = multiprocessing.Process(target=localServer)
    server.start()
    client.start()
    time.sleep(15)
    # 客户端关闭，但是服务端没有关闭，可以一直等待消息
    client1 = multiprocessing.Process(target=localClient)
    client1.start()
    # 在vscode中通过 multiprocessing.Process开辟的新进程是守护进程（主程序结束就会退出，所以此处需要等待，在idea中不需要）
    time.sleep(25)
