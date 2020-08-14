#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 
urllib提供了一系列用于操作URL的功能，可以使用第三方模块 request，更方便
version: 1.0
Author: xieyupeng
Date: 2020-08-11 18:12:59
LastEditors: xieyupeng
LastEditTime: 2020-08-13 10:53:49
'''
from urllib import request
from urllib import parse


def getTest():
    with request.urlopen('http://www.baidui.com/') as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', data.decode('utf-8'))


def postTest(email, passwd):
    login_data = parse.urlencode([
        ('username', email), ('password', passwd), ('entry', 'mweibo'),
        ('client_id', ''), ('savestate', '1'), ('ec', ''),
        ('pagerefer',
         'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F'
         )
    ])

    req = request.Request('https://passport.weibo.cn/sso/login')
    req.add_header('Origin', 'https://passport.weibo.cn')
    req.add_header(
        'User-Agent',
        'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'
    )
    req.add_header(
        'Referer',
        'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
    )

    with request.urlopen(req, data=login_data.encode('utf-8')) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))


if __name__ == "__main__":
    # getTest()
    print('Login to weibo.cn...')
    email = input('Email:')
    passwd = input('password:')
    postTest(email, passwd)
