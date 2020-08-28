<!--
 * @Descripttion: 
 * @version: 1.0
 * @Author: xieyupeng
 * @Date: 2020-08-07 16:53:38
 * @LastEditors: xieyupeng
 * @LastEditTime: 2020-08-27 13:50:25
-->
# 前端开发工具
- vsCode
- webstom
- sublime

# vsCode
- 微软用js开发的一款编辑器，可以通过丰富的插件实现ide的功能
- 引用另外一个文件的方法时，不能点击跳转过去，不知如何配置
- 单击文件只是预览，文件名是斜的；双击才能固定在编辑器，此时文件名是正的
- svn修改过的文件及父目录没有做变色处理，git有
- 如果直接在工作区打开文件，每次只能打开一个文件夹；工作区右键，把文件夹添加到工作区，就可以添加多个文件夹；
- debuggerforchrome，在debug界面配置对应项目的launch.json文件，修改端口号；在某个项目文件的编辑页面，按F5自动跳转到浏览器
- markdown toc 自动生成目录时会乱码， 是因为vscode默认行尾字符是auto，在设置-用户设置页面，搜索eol，修改行尾字符为\n
- 调试：如果工作空间只有一个项目，只能添加配置在工作空间公共区域；如果有多个项目，可以在每个项目中配置
- vscode工作目录默认是项目根目录，所以在文件中调用相对路径下的文件会找不到，通过launch.json配置"cwd": "${fileDirname}"，把文件所在目录作为工作目录

# vsCode常用快捷键
- Ctrl+shift+E 项目结构
- Ctrl+shift+F 全局搜索
- Ctrl+shift+G 版本控制
- Ctrl+shift+D 调试
- Ctrl+B：打卡左侧功能区
- Ctrl+shift+P（F1）：所有命令
- Ctrl+P：搜索文件
- Ctrl+`：终端
- Ctrl+j：控制台隐藏展示
- F2：重名名，所有用到的地方都会修改
- F3：查找，但是光标还在编辑器内，可以直接编辑，巧妙方便
- F12：打开引用链，只限当前文件
- Ctrl+\:新增一个编辑器，并把当前文件复制一份
- Ctrl+1/2：在两个编辑器之间切换
- Alt+↑↓：移动代码
- Alt+Shift+↑↓：复制代码
- 同sublime快捷键：
    - Ctrl+shift+T：打开最近关闭页面
    - Ctrl+H：查找和替换，光标是在搜索框内
    - Ctrl+W：关闭当前页面
    - Ctrl+N：打开一个新页面
    - Ctrl+-/=：放大缩小
    - Ctrl+Enter：换行
    - Ctrl+Alt+↑↓：多个光标，然后通过home或end统一位置
    - Ctrl+Up/Down：在所有文件间切换，可以跨编辑器

- 自定义快捷键：
    - Ctrl+D：删除一行
    - 清除markdown快捷键：Ctrl+B
    - 清楚gitlens所有快捷键

# typescript
微软开发和维护的一套编程语言，包含了js所有的元素，扩展了js的语法，加入了类，函数，模块等概念，用于大型项目开发

# vscode整合python环境
- vscode插件：
  - python
- python插件：
  - 国内镜像：https://mirrors.aliyun.com/pypi/simple/
  - flake8(代码语法检测)
  - yapf(代码格式化)
  - rope(代码重构)
- vscode配置：
  - settings.json(python环境配置)
  - launch.json(python调试配置) 