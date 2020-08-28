#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 使用aiohttp框架，建立基本请求响应模式
version: 1.0
Author: xieyupeng
Date: 2020-08-27 13:42:17
LastEditors: xieyupeng
LastEditTime: 2020-08-27 15:08:21
'''
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)
routes = web.RouteTableDef()

#  1、定义URL映射
@routes.get('/')
def index(request):
    return web.Response(body=b'<h1>Awesome App</h1>', content_type='text/html')

# 2、启动服务器
def init():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    logging.info('server started at http://127.0.0.1:9000...')
    web.run_app(app, host='127.0.0.1', port=9000)

init()