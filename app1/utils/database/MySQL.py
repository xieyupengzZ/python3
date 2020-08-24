#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 
安装 MySQL驱动 pip install mysql-connector-python -i https://mirrors.aliyun.com/pypi/simple/
安装 ORM框架 pip install sqlalchemy -i https://mirrors.aliyun.com/pypi/simple/

version: 1.0
Author: xieyupeng
Date: 2020-08-24 17:41:39
LastEditors: xieyupeng
LastEditTime: 2020-08-24 18:35:56
'''

import mysql.connector
from sqlalchemy import Column, String, create_engine,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

def mysqlop():
    
    conn = mysql.connector.connect(user='root',                             
                                   password='xieyupeng',
                                   database='heartbeatnet')                                 # 1 用户，口令，数据库
    
    cursor = conn.cursor()                                                                  # 2 开启一个游标
    cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')      
    cursor.execute('insert into user (id, name) values (%s, %s)',['1', 'xieyupeng'])        
    print(cursor.rowcount)                                                                  # 输出影响条数
    conn.commit()                                                                           # 3 提交事务
    cursor.close()                                                                          # 4 一个事务结束后最好关闭游标

    cursor = conn.cursor()                                                                  # 5 重新开启一个查询的游标
    cursor.execute('select * from user where id = %s', ('1', ))
    print(cursor.fetchall())                                                                # 输出查询条数
    cursor.close()                                                                          

    conn.close()                                                                            # 6 关闭Connection


def mysqlORM():

    Base = declarative_base()                                                                       # 创建对象的基类:
    
    class User(Base):                                                                               # 定义User对象:
        __tablename__ = 'user'                                                                      # 表名称

        id = Column(String(20), primary_key=True)                                                   # 表的结构:
        name = Column(String(20))
        teacher = relationship('Teacher')                                                           # 关联teacher表（写的是模型名称）

    class Teacher(Base):
        __tablename__ = 'teacher'                                                                      

        id = Column(String(20), primary_key=True)                                                   
        name = Column(String(20))
        user_id = Column(String(20), ForeignKey('user.id'))                                         # 一对多，多的那一方，通过外键关联

    engine = create_engine('mysql+mysqlconnector://root:xieyupeng@localhost:3306/heartbeatnet')     # 初始化数据库连接:
    Base.metadata.create_all(engine)                                                                # 创建表结构
    DBSession = sessionmaker(bind=engine)                                                           # 创建DBSession类型，相当于开启数据库连接

    session = DBSession()                                                                           # 创建session对象插入数据
    new_user = User(id='1', name='xieyupeng')                                                       # 创建新User对象:
    session.add(new_user)                                                                           # 添加到session:                       
    session.commit()                                                                                # 提交即保存到数据库:
    session.close()                                                                                 # 关闭session:

    session = DBSession()                                                                           # 创建session对象查询数据            
    user = session.query(User).filter(User.id == '1').one()                                         # one()返回唯一行，all()则返回所有行
    print('type:', type(user))
    print('name:', user.name)
    session.close()                                                                                 # 关闭Session:

if __name__ == "__main__":
    # mysqlop()
    mysqlORM()