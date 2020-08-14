#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-14 14:22:01
LastEditors: xieyupeng
LastEditTime: 2020-08-14 16:02:31
'''

import requests


# requests.get
# 状态码：418，原因：反爬虫程序，解决：设置 headers
def getTest():
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host":
        "www.douban.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }
    res = requests.get('http://www.douban.com/', headers=headers)
    print("状态码：", res.status_code)
    print("请求URL：", res.url)
    print("响应头：", res.headers)
    # print('页面HTML：',res.text)
    print('页面内容：', res.content)


# requests.get 
# 入参：params
def getParamsTest():
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host":
        "www.douban.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }
    params = {"q": "python", "cat": '1001'}
    res = requests.get('http://www.douban.com/search',
                       headers=headers,
                       params=params)
    print("状态码：", res.status_code)
    print("响应头：", res.headers)
    print("请求URL：", res.url)
    # print('页面HTML：', res.text)


# requests.post 
# 可以通过 data 入参，也可以通过 json 入参
def postTest():
    url = ''
    res = requests.post(url,data={},json={})

# 方便的上传文件
def postFileTest():
    url = ''
    openFile = {'file':open('../processfiles/code.jpg','rb')}
    res = requests.post(url,file=openFile)

if __name__ == "__main__":
    # getTest()
    getParamsTest()