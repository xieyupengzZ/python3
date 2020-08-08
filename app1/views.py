from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os


def output(request):
    # return HttpResponse(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 如果此处指向一个页面，需要配置 python1 的 settings.py，TEMPLATES - DIRS 中加入网页的目录
    return render(request, 'hello.html')


def show(request):
    return render(request, 'show.html')
