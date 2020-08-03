from django.conf.urls import url

# 从当前目录导入views.py
from . import views

urlpatterns=[
    url('hello/',views.output),
    url('show/',views.show)
]