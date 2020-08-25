#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: flask框架
flask框架下载：pip install flask -i https://mirrors.aliyun.com/pypi/simple/
version: 1.0
Author: xieyupeng
Date: 2020-08-25 17:40:37
LastEditors: xieyupeng
LastEditTime: 2020-08-25 17:42:38
'''

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form[
            'password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'


if __name__ == '__main__':
    app.run()