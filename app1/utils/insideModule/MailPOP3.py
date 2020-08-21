#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 收邮件
协议：POP
模块：poplib（接受邮件）,email（解析邮件）
登陆qq邮箱，进入设置-账户，开启SMTP服务，可以得到对应的密码（IMAP/POP3）
version: 1.0
Author: xieyupeng
Date: 2020-08-21 15:29:12
LastEditors: xieyupeng
LastEditTime: 2020-08-21 18:05:18
'''
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def getMail():
    # 输入邮件地址, 口令和POP3服务器地址:
    email = '1107761900@qq.com'
    password = 'cljzkrdzifbjghib'
    pop3_server = 'pop.qq.com'

    # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    # 身份认证:
    server.user(email)
    server.pass_(password)

    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)

    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件(MIME对象，需要额外解析):
    msg = Parser().parsestr(msg_content)
    print_info(msg)
    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()

# 邮件解析
def print_info(msg):
    decodeMailHeader(msg)
    decodeMailParts(msg)
    

# 解析邮件头部
def decodeMailHeader(msg):
    print('--------------------')
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':  # 标题
                value = decode_str(value)
            else:  # 发件人和收件人
                hdr, addr = parseaddr(value)  # 名称和邮件地址
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
        print('%s: %s' % (header, value))

# 解析邮件内容
def decodeMailParts(msg):
    if (msg.is_multipart()):    # 是否有多个部分组成
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('--------------------')
            print('part %s' % (n))
            decodeMailParts(part)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('Text: %s' % (content + '...'))
        else:
            print('Attachment: %s' % (content_type))

# 解析头部字符串
def decode_str(str):
    value, charset = decode_header(str)[0]
    if charset:
        value = value.decode(charset)
    return value

# 获取内容编码
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


if __name__ == "__main__":
    getMail()