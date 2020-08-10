

# 1. **一级标题**
## 1.1. 二级标题


# 2. **段落**

## 2.1. 换行：
末尾加两个空格  

## 2.2. 斜体：
*斜字符串1* _斜字符串2_

## 2.3. 粗体：
**粗字符串1** __粗字符串2__

## 2.4. 分隔：
***
* * *
- - -
---

## 2.5. 删除：
~~xieyupengzZ~~

## 2.6. 下划：
<u>下划线</u>

## 2.7. 转义：
> 以下符号前加上 \ 实现原样输出：
>> \   反斜线  
>> `   反引号  
>> \*   星号  
>> _   下划线  
>> {}  花括号  
>> []  方括号  
>> ()  小括号  
>> \#   井字号  
>> \+   加号  
>> \-   减号  
>> .   英文句点  
>> !   感叹号  

## 2.8. HTML标签：
目前支持：`<kbd> <b> <i> <em> <sup> <sub> <br>`  
markdown使用 <kbd>Ctrl</kbd> + <kbd>K</kbd> + <kbd>V</kbd> 预览效果

# 3. 表格
第一列|第二列|第三列
:-|-:|:-:
1-1|1-2|1-3
2-1|2-2|1-3

# 4. 列表

* 第一点，此处使用星号
* 第二点，还可以用 - 或 + 
    * 第二小点

1. 第一点
2. 第二点
3. 第三点

- [ ] 选项一
- [x] 选项二

# 5. 区块
> 引用1  
> 引用2  

> 引用3  
>> 引用4  
>>> 引用4

> - 引用1  
> - 引用2  

+ 第一点
    > 引用1  
    > 引用2

# 6. 代码
引用函数：`namedtupleTest`
```python
def namedtupleTest():

    point = namedtuple('Point',['x','y'])
    p = point(1,2)
    print('命名型元组 ',p)
    print(p.x,p.y)

    p1 = (1,2)
    print('普通元组 ',p1)
    print(p1[0],p1[1])
```

# 7. 链接
[百度](http://www.baidu.com)(想要跳转外部连接必须加上http，否则以当前项目根目录作为相对地址)
<www.baidu.com>(这样就不需要http)

这个链接用 1 作为网址变量 [Google][1]  
这个链接用 runoob 作为网址变量 [Runoob][]  
然后在文档的结尾为变量赋值  

[1]: http://www.google.com/
[Runoob]: http://www.runoob.com/

脚注：Markdown[^1]  

[^1]: Markdown是一种纯文本标记语言

# 8. 图片
![加载不出时展示的名称](http://static.runoob.com/images/runoob-logo.png "鼠标悬浮标题展示")

<img src="http://static.runoob.com/images/runoob-logo.png" width="100%">

[![加载不出时展示的名称](http://static.runoob.com/images/runoob-logo.png "鼠标悬浮标题展示")](http://static.runoob.com/images/runoob-logo.png)

# 9. 视频
<iframe height=498 width=510 src='http://player.youku.com/embed/XMjgzNzM0NTYxNg==' frameborder=0 'allowfullscreen'></iframe>

# 10. 数学公式
$
\mathbf{V}_1 \times \mathbf{V}_2 =  \begin{vmatrix} 
\mathbf{i} & \mathbf{j} & \mathbf{k} \\
\frac{\partial X}{\partial u} &  \frac{\partial Y}{\partial u} & 0 \\
\frac{\partial X}{\partial v} &  \frac{\partial Y}{\partial v} & 0 \\
\end{vmatrix}
$