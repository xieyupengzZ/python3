'''
Descripttion: 
解析标签文件xml
1、DOM，把整个文件读进内存，占内存，解析慢
2、SAX，流模式，边读边解析，不占内存，解析快
解析标签文件html
HTMLParser
version: 1.0
Author: xieyupeng
Date: 2020-08-12 09:58:00
LastEditors: xieyupeng
LastEditTime: 2020-08-12 14:53:35
'''
from xml.parsers.expat import ParserCreate
from html.parser import HTMLParser


# 定义一个类，用SAX解析xml文件
class SaxHandler():
    # 读取开始节点 及 属性信息
    def start_element(self, name, attrs):
        print('SAX:start: %s , attrs: %s' % (name, attrs))

    # 读取节点内容
    def end_element(self, name):
        print('SAX:end: %s ' % name)

    # 读取结束节点
    def char_data(self, text):
        print('SAX:char: %s' % text)


def parseXml():
    xml = r'<?xml version="1.0"?><ol><li><a href="/python">Python</a></li><li><a href="/ruby">Ruby</a></li></ol>'
    handler = SaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)


# 定义一个类，解析hmtl文件
class myHTMLParser(HTMLParser):
    # 开始标签
    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    # 结束标签
    def handle_endtag(self, tag):
        print('</%s>' % tag)

    # 开始和结束在一起的标签
    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    # 注解
    def handle_comment(self, data):
        print('注解：', data)

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


def parseHtml():
    parser = myHTMLParser()
    parser.feed('''
    <html><head></head><body>
    <!-- 注解写在这里 -->
    <p>Some <a href="#">html</a> HTML&nbsp;tutorial...<br>END</p>
    </body></html>''')


if __name__ == "__main__":
    parseHtml()
