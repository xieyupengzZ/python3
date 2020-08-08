"""python1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''
路由层
URL与视图函数之间的映射关系
如果urlpatterns中只有一个映射，那么直接访问 http://127.0.0.1:8000/ 默认就是这个路径
如果存在多个映射，那么必须在后面加上路径
'''
from django.contrib import admin
from django.urls import path, include

from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/',views.output), # 只映射某一个路径
    path('app1/', include('app1.urls')),  #把整个app1项目中的映射都添加过来
]
