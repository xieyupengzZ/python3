'''
Descripttion: 操作图片
version: 1.0
Author: xieyupeng
Date: 2020-08-13 10:54:59
LastEditors: xieyupeng
LastEditTime: 2020-08-14 14:21:05
'''
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from PIL import ImageFont
import random


def operateImage():

    # 打开一个jpg图像文件，注意是当前路径:
    im = Image.open('../processfiles/editor.jpg')

    # 获得图像尺寸:
    w, h = im.size
    print('image size: %sx%s' % (w, h))

    # 缩放到50%:
    im.thumbnail((w / 2, h / 2))
    print('Resize image to: %sx%s' % (w / 2, h / 2))
    im.save('../processfiles/editor1.jpg', 'jpeg')

    # 通过imageFilter实现模糊效果，还有如切片，选择，滤镜等功能都可以尝试
    im2 = im.filter(ImageFilter.BLUR)
    im2.save('../processfiles/editor2.jpg', 'jpeg')


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64,255), random.randint(64,255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32,127), random.randint(32,127), random.randint(32, 127))


# 验证码绘图
def imageDraw():

    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # 读取 otf 或 ttf字体文件
    font = ImageFont.truetype('../processfiles/MyfridaBold.otf',size=40)
    ImageFont
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字
    for t in range(4):
        draw.text((t * 60 + 10, 10), rndChar(), font=font,fill=rndColor2())
    image.save('../processfiles/code.jpg', 'jpeg')


if __name__ == "__main__":
    # operateImage()
    imageDraw()