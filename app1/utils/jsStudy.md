## 基本数据类型
- Number，浮点数和整数
- boolean，true和flase
- 字符串 
  - 不可变，对字符串的操作，都是返回一个新的字符串，不影响原来的字符串
  - 常用属性，length
  - 常用方法，toUpperCase(),toLowerCase(),indexOf(),substring()
  - >NaN是Number，它不等于任何值（包括它自己），用isNaN()来判断。
    >null 表示变量没有指向任何地址，undefined 表示变量没有被赋值。  
    >null 和 undefined的值相同，但是类型不同。   
    >一个变量声明后默认值就是 undefined
## 运算符
- 逻辑运算符，&& || ! 
- 比较运算符 
  - == 自动转换类型比较，有时会得到诡异的结果
  - === 不自动转换类型，数据类型不一致false，建议使用此方式
## 数组
- 两种创建方式：[ ]，new Array()
- 数组的索引其实就是数组作为一个对象的属性，通过for...in遍历时可以看出
- 常用属性，length
- 常用方法，indexOf(),join(),slice(),push(),pop(),unshift(),shift()
- >通过索引赋值，a[5]=8，如果索引大于数组长度，会导致数组自动扩容。   
  >通过长度赋值，a.length=8，如果索引大于数组长度，会导致数组自动扩容
## 对象
- 格式类似json，和json不一样
- 对象格式如下：{ name: 'Bob',age: 20 } 
- json格式如下：{ 'name':'Bob','age':20 }
- 访问不存在属性返回undefined
- 判断一个属性是否存在：
  - in：包含继承属性
  - hasOwnProperty()：只判断自身的属性
## 变量
- 定义规则和 java 一样
- 定义规则：由 数字，字母，_，$ 组成，数字不能打头，不能使用关键字
- 动态语言：变量类型声明后，可以赋值任何类型的值，如 js，java不行
## for
- 遍历数组：for(var i = 0 , len = array.lenght ; i < len ; i ++)
- 遍历通用方法：for(var i in object)：
  - 此方法遍历对象时：i 表示属性
  - 此方法遍历json对象时：i 表示key（key其实就是json对象的属性）
  - 此方法遍历数组是：i 表示索引（索引其实就是数组对象的属性）
## ES6新标准
- 新增的数据类型：iterable，Map，Set
- Map，set，array 都属于 iterable
- for...of 用来遍历 iterable，for...in 遍历的是属性，for...of遍历的是值
## 函数
- 如果没有 return 语句，默认返回 undefined
- 关键字 arguments：
    - 只在函数内部生效，指向函数所有入参，包括函数未接受的参数
    - 类似array，但不是array，可以通过 length 获取参数个数