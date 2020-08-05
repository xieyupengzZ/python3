from collections import namedtuple,deque,defaultdict,OrderedDict,Counter,ChainMap


'''
命名型元组，方便定义元组的业务用途，规定了元组的名称，属性名称以及个数
普通元组通过索引来引用元素，命名型元组可以通过属性来引用元素
'''
def namedtupleTest():

    point = namedtuple('Point',['x','y'])
    p = point(1,2)
    print('命名型元组 ',p)
    print(p.x,p.y)

    p1 = (1,2)
    print('普通元组 ',p1)
    print(p1[0],p1[1])



'''
list 线性存储，按索引访问元素很快，但是插入和删除元素就很慢
deque 是为了高效实现插入和删除操作的双向列表，适合用于队列和栈
'''
def dequeTest():

    dq = deque(['xie'])                     # 新建
    # dq = deque(('xie',))
    dq.append('zhang')                      # 尾部新增
    dq.appendleft('pang')                   # 首部新增
    print(dq)
    dq.pop()                                # 尾部删除
    dq.popleft()                            # 首部删除
    print(dq)
    dq.insert(4,'peng')                     # 如果索引大于列表长度，默认放在索引最后
    print(dq)
    print('xie的位置：',dq.index('xie'))     # 如果存在多个，默认返回第一个位置；如果不存在，报错！！！！
    print('xie的数量：',dq.count('xie'))
    dq1 = dq.copy()
    print('复制列表：',dq1)
    xyp = ('zhang','pang')
    dq.extend(xyp)                          # 添加一个可迭代对象，内部是循环每个元素顺序调用append
    dq.extendleft(xyp)                      # 因为是循环一个个调用appendleft，所以最终加入列表的效果是倒序的，具体查看输出可知
    print('合并列表：',dq)
    dq.remove('pang')                       # 如果存在多个，默认删除第一个关键字；如果不存在，报错！！！！
    dq.remove('zhang')
    print(dq)
    dq.reverse()
    print('倒序列表：',dq)
    dq.clear()                              # 清空列表
    print(dq)



'''
dict 访问不存在的key，会报错
defaultdict 访问不存在的key，返回默认值

dict 的key不能保证是有序的（3.5版本无序，3.6、3.7是有序）
orderedDict 可以保持key的插入顺序
输出有序不代表保证是有序的，想要确定是有序的，必须用OrderedDict

Counter是一个简单的计数器，统计字符个数，本质也是一个dict
'''
def dictTest():

    def defaultInfo():                              # 必须定义一个函数返回默认值
        return 'NOT FOUND'
    dd = defaultdict(defaultInfo)
    dd['name'] = 'xyp'
    print(dd['name'])                               # 访问存在的key
    print(dd['age'])                                # 访问不存在的key

    d = dict([('a',1),('b',2),('c',3)])
    print(d)                                        # 此处使用的是3.7版本，所以普通的dict也是有序
    od = OrderedDict([('a',1),('b',2),('c',3)])
    print(od)                                       # 输出OrderedDict

    c = Counter('xieyupengzhangpangpnag')           # 字符为key，个数为value，组成的dict（默认根据个数大小排序）
    print('通过字符串创建：',c)
    c1 = Counter(d)
    print('通过字典创建：',c1)

'''
多个dict，组成一个逻辑上的dict
如：寻找解决生产问题的人员，有三个类别，实习生，开发工程师，主管工程师，
    优先从主管工程师中找，如果找不到，再从开发工程师找，最后实习生顶上
'''
def chainMapTest():
    sxs = dict({'java':'szb','caiji':'szb'})
    kf = dict({'java':'xyp','kafka':'tyj'})
    zg = dict({'java':'zxf','caiji':'hyq'})

    cm = ChainMap(zg,kf,sxs)                        # 从多个dict中查找，优先级从左到右，直到找到对应的key

    print('解决生产java问题：',cm['java'])
    print('解决生产kafka问题：',cm['kafka'])
    print('解决生产采集问题：',cm['caiji'])



if __name__ == '__main__':
    # namedtupleTest()
    # dequeTest()
    dictTest()
    # chainMapTest()