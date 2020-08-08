'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-01 18:55:27
LastEditors: xieyupeng
LastEditTime: 2020-08-08 19:04:37
'''
from django.contrib import admin

# Register your models here.
from . import models

# 在网上搜都是 admin.site.register， 坑啊


class mqSet(admin.ModelAdmin):
    list_display = ['英文名', '中文名', '公司']


admin.register(models.messageQueue, mqSet)
