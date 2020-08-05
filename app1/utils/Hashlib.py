'''
hashlib提供了常用的摘要算法（单向算法）
摘要算法：通过摘要函数，对任意长度的数据，计算出固定长度的摘要，可以检测原数据被人篡改
MD5：固定128bit，通常用 32位 16进制字符串，【1个16进制占4bit】
SHA1：固定160bit，通常用 40位 16进制字符串，SHA256和SHA512更安全，但是计算更慢
MD5加盐：防止用户定义一个简单的字符串，MD5编码时默认在原字符串上加一个固定的复杂字符串

hmac，可以看做MD5加盐的升级版，把盐当做一个秘钥，对原字符串编码，而不是简单的字符串拼接，而且针对所有哈希算法
'''
import hashlib
import hmac

md5 = hashlib.md5()
md5.update('my name is xieyupeng,i is studying python!'.encode('utf-8'))
print(md5.hexdigest())

md5.update('my name is xieyupeng,'.encode('utf-8'))                     # 可以分批update
md5.update('i is studying python!'.encode('utf-8'))
print(md5.hexdigest())

md5.update(('my name is xieyupeng'+'jiayan+_&@*').encode('utf-8'))      # MD5加盐
print('md5加盐：',md5.hexdigest())

sha1 = hashlib.sha1()
sha1.update('my name is xieyupeng,i is studying python!'.encode('utf-8'))
print('sha1：',sha1.hexdigest())

sha256 = hashlib.sha256()                                               # 更安全，但是更慢
sha256.update('my name is xieyupeng,i is studying python!'.encode('utf-8'))
print('sha256：',sha256.hexdigest())

sha512 = hashlib.sha512()                                               # 更安全，但是更慢
sha512.update('my name is xieyupeng,i is studying python!'.encode('utf-8'))
print('sha512：',sha512.hexdigest())

msg = b'python is so butifual!'
key = b'!@#$%'
h = hmac.new(key,msg,digestmod='MD5')
print('hmac实现带key哈希：',h.hexdigest())
