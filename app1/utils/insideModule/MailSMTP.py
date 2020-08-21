#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 发邮件
协议：SMTP
模块：email（构造邮件），smtplib（发送邮件）
流程：发件人 -> MUA -> MTA -> MTA -> ... -> MDA <- MUA <- 收件人
MUA：邮件软件（qq邮箱，google邮箱）
MTA：邮件传输代理
MDA：邮件投递代理（服务器）
version: 1.0
Author: xieyupeng
Date: 2020-08-20 17:46:02
LastEditors: xieyupeng
LastEditTime: 2020-08-21 15:28:26
'''
from email import encoders
from email.utils import formataddr
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart,MIMEBase
import smtplib

'''
msg: 发送邮件公共方法 
mail: 邮件对象
send: 发件人名称
to: 接收人名称
title: 邮件标题
'''
def sendEmail(mail,send,to,title):
    # 发件人地址
    from_addr = '1107761900@qq.com'
    # 口令(在qq邮箱设置中开启SMTP时获取的密码)
    password = 'iskamhtiwsumggbe'
    # 收件人地址:
    to_addr = '1107761900@qq.com'
    # SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    # 邮件头部-发送者（邮件界面右下角新邮件弹窗时，显示发件人是 send，但是进入邮件后，发件人和接受人都是根据 from_addr和to_addr 展示对应的 qq用户名
    mail['From'] = formataddr((send,from_addr))
    # 邮件头部-接受者(收件人会展示 to_addr的用户名)
    mail['To'] = formataddr((to,to_addr))
    # 邮件头部-标题
    mail['Subject'] = Header(title, 'utf-8')
    # 发送邮件
    # server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server = smtplib.SMTP_SSL(smtp_server, 465)  # SMTP_SSL 协议默认端口是465
    server.login(from_addr, password)
    server.set_debuglevel(1)  # 打印所有和服务器交互的日志
    server.sendmail(from_addr, [to_addr], mail.as_string())
    server.quit()


def sendTextEmail():
    # 构造邮件内容
    mail = MIMEText(
        'hello，my name is 谢宇鹏...',  # 正文
        'plain',  # 类型，此处表示纯文本（其他类型：HTML)
        'utf-8'  # 编码
    )
    sendEmail(mail,'python-谢宇鹏','谢宇鹏','python发送的邮件')


def sendAttachEmail():

    # 创建带附件的实例
    mail = message = MIMEMultipart()

    # 邮件内容，可以引用附件中图片，根据 Content-ID 引用
    mail.attach(
        MIMEText(
            '<html><body><h1>Hello</h1>' +
            '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
            '<p><img src="cid:1"></p>' +
            '</body></html>', 'html', 'utf-8'))

    # 文本附件
    att = MIMEText(
        open('../insideModule/MailSMTP.py', 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="MailSMTP.py"'
    mail.attach(att)

    # 图片附件
    with open('../processfiles/editor.jpg','rb') as imageAtt:
        # 设置附件的MIME和文件名
        mime = MIMEBase('image', 'jpeg', filename='editor.jpg')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='editor.jpg')
        mime.add_header('Content-ID', '<1>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(imageAtt.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        mail.attach(mime)

    sendEmail(mail,'python-谢宇鹏','谢宇鹏','python发送的附件')


if __name__ == "__main__":
    # sendTextEmail()
    sendAttachEmail()