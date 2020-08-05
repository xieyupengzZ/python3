

'''
Base64，是对二进制数据进行编码的一种方式，所有用来编码的字符只有64个，不能用做加密
编码后的二进制数据如果不是3的倍数，会在结尾加上\x00补充，再在末尾加上=号，表示补了多少个字节

url safe : 把 + 和 / 替换成 - 和 _，因为标准Base64编码后的字符 + /，在URL中是不能当做参数的
在URL、Cookie里面会造成歧义 = 会造成歧义，所以，很多Base64编码后会把 = 去掉，解码的时候记得加上
'''

import base64
print(base64.b64encode(b'xieyupeng&zhangpang'))
print(base64.b64decode('eGlleXVwZW5nJnpoYW5ncGFuZw=='))

print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))

base64.decode('','')                            # 解码一个文件，写入另一个二进制文件
base64.encode('','')                            # 编码一个文件，写入另一个二进制文件
