#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 
SQLite的数据库其实就是一个文件，是用C开发的，体积小，可以集成到APP中，轻量，不支持高并发
pytho内置SQLite，可以直接使用
version: 1.0
Author: xieyupeng
Date: 2020-08-24 10:55:58
LastEditors: xieyupeng
LastEditTime: 2020-08-24 17:41:10
'''
import sqlite3


def createUserTable():
    try:
        # 连接到SQLite数据库，数据库文件是test.db，如果文件不存在，自动创建
        conn = sqlite3.connect('../processfiles/sqliteTest.db')
        # 创建一个Cursor:
        cursor = conn.cursor()
        # 执行一条SQL语句，创建user表:
        cursor.execute(
            'create table user (id varchar(20) primary key, name varchar(20))')
        # 提交事务:
        conn.commit()
    except Exception as e:
        print('异常类型：%s 异常信息：%s ' % (type(e), e))
        # 异常回滚数据
        conn.rollback()
    finally:
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()


def insertUser(userdata):
    try:
        # 连接到SQLite数据库，数据库文件如果不存在，自动创建
        conn = sqlite3.connect('../processfiles/sqliteTest.db')
        # 创建一个Cursor:
        cursor = conn.cursor()
        # 执行一条SQL语句，插入记录:
        insertSql = 'insert into user (id, name) values'
        for user in userdata:
            insertSql = insertSql + str(user) + ','
        insertSql = insertSql[:-1]  # 字符串截取，从开始到倒数第二个，半闭半开，所以结尾指向倒数第一个位置
        print('插入语句：', insertSql)
        cursor.execute(insertSql)
        # 提交事务:
        conn.commit()
        # 通过rowcount获得插入的行数:
        print('成功插入 %s 条' % cursor.rowcount)
    except Exception as e:
        print('异常类型：%s 异常信息：%s ' % (type(e), e))
        # 异常回滚数据
        conn.rollback()
    finally:
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()


def queryUser(userId='0'):
    try:
        conn = sqlite3.connect('../processfiles/sqliteTest.db')
        cursor = conn.cursor()
        # 执行查询语句:
        if (userId == '0'):
            cursor.execute('select * from user')
        else:
            cursor.execute('select * from user where id = ?', (userId, ))
        # 获得查询结果集:
        print(cursor.fetchall())
    except Exception as e:
        print('异常类型：%s 异常信息：%s ' % (type(e), e))
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # userdata = [("1", "xieyupeng"), ("2", "zhangzhao")]
    # insertUser(userdata)
    queryUser()