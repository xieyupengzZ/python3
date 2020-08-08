'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-01 18:55:27
LastEditors: xieyupeng
LastEditTime: 2020-08-08 19:06:38
'''
from django.conf.urls import url

# 从当前目录导入views.py
from . import views

urlpatterns = [url('hello/', views.output), url('show/', views.show)]
