'''
Descripttion: 
version: 1.0
Author: xieyupeng
Date: 2020-08-05 22:24:51
LastEditors: xieyupeng
LastEditTime: 2020-08-08 18:51:55
'''


def fileRead():

    try:
        f = open('C:\\Users\\Administrator\\Desktop\\file.txt', 'r')
        print('第一次读：', f.read())
        print(f.mode)  # 模式
        print(f.name)  # 文件路径和名字
        print(f.readable())  # 是否可读
        print(f.writable())  # 是否可写
        print(f.tell())  # 下次读写开始的位置
        print('第二次读：', f.read())
        print(f.seekable())  # 是否可移动光标
        print(f.seek(0, 0))  # 光标移到开始位置
        print('第三次读：', f.read())

    except FileNotFoundError as e:
        print('异常捕捉了')
        raise FileNotFoundError('file not exist')

    except Exception as e:
        print('异常捕捉了')
        raise e

    finally:
        if f:
            f.close()


'''

with方法相当于 try catch except finally 方法的简写

r： 开始，读
r+：开始，读，  写(替换对应位置字符)
w： 开始，不读, 写(创建文件，删除原内容)
w+：开始，读，  写(创建文件，删除原内容)
a： 结尾，不读, 写(创建文件，追加新内容)
a+：结尾，读，  写(创建文件，追加新内容)

read()         一次性读取文件的全部内容，如果文件过大，内存就爆了
read(size)     一次读取size大小的内容
readline()     每次读取一行内容
readlines()    读取所有内容，得到list，一个元素表示一行

'''


def fileReadWith(type):
    with open('C:\\Users\\Administrator\\Desktop\\file.txt', type) as f:
        for i in range(100):
            if i % 2 == 0:
                f.write('xieyupeng')
            else:
                f.write('zhangzhao \n')  # 换行符 \n 占两个字符

    with open('C:\\Users\\Administrator\\Desktop\\file.txt', type) as f:
        for i in f.readlines():
            print(i.strip())  # strip去空格


if __name__ == '__main__':
    fileReadWith('r+')
    # fileRead()