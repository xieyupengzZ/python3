#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 系统监控
version: 1.0
Author: xieyupeng
Date: 2020-08-14 16:19:17
LastEditors: xieyupeng
LastEditTime: 2020-08-14 17:00:09
'''
import psutil


def psutilTest():
    # print('CPU逻辑数量：', psutil.cpu_count())
    # print('CPU物理核心：', psutil.cpu_count(logical=False))
    # print('CPU时间：', psutil.cpu_times())
    # print('CPU使用率：', psutil.cpu_percent(interval=1, percpu=True))
    # print('CPU内存信息：',psutil.virtual_memory())
    # print('CPU磁盘分区：',psutil.disk_partitions())
    # print('CPU磁盘使用：',psutil.disk_usage('C:/'))
    # print('CPU磁盘IO：',psutil.disk_io_counters())
    print('网络接口信息：', psutil.net_if_addrs())
    print('进程ID：', psutil.pids())
    p = psutil.Process(1896)
    print(
        '根据ID获取进程信息：\n 进程名称 %s ，\n exe路径 %s ，\n 进程状态 %s  ，\n 进程用户名 %s ，\n 进程创建时间 %s ，\n 占用CPU时间 %s ，\n 占用内存 %s ，\n 线程数量 %s \n'
        % (p.name(), p.exe(), p.status(), p.username(), p.create_time(),
           p.cpu_times(), p.memory_info(), p.num_threads()))


if __name__ == "__main__":
    psutilTest()