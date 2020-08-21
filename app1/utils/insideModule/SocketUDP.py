#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: UDP编程，不可靠连接，只负责发送，不负责到达，优势就是比TCP快
UDP端口和TCP端口不冲突，可以重复
version: 1.0
Author: xieyupeng
Date: 2020-08-20 16:14:16
LastEditors: xieyupeng
LastEditTime: 2020-08-20 16:46:02
'''
import socket
import multiprocessing
import time

def localServer():

    # SOCK_DGRAM UDP协议
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定端口:
    s.bind(('127.0.0.1', 9999))
    # UDP不需要 listen()
    print('server:Bind UDP on 9999...')
    while True:
        # 接收数据:
        data, addr = s.recvfrom(1024)
        print('server:Received from %s:%s.' % addr)
        s.sendto(b'Hello, %s!' % data, addr)


def localClient():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for data in [b'Michael', b'Tracy', b'Sarah']:
        # 发送数据:
        print('client:send ',data)
        s.sendto(data, ('127.0.0.1', 9999))
        # 接收数据:
        print('client:',s.recv(1024).decode('utf-8'))
    s.close()

if __name__ == "__main__":
    server = multiprocessing.Process(target=localServer)
    client = multiprocessing.Process(target=localClient)
    server.start()
    time.sleep(1)
    client.start()
    time.sleep(10)