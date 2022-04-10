'''
Author: 七画一只妖
Date: 2022-03-25 18:21:45
LastEditors: 七画一只妖
LastEditTime: 2022-04-10 10:56:51
Description: file content
'''

import os
from PIL import Image, ImageDraw, ImageFont

current_path = os.path.dirname(os.path.abspath(__file__))

# 字体路径
font_path = f"{current_path}/data/yuanshen.ttf"

# 图片保存路径
save_path = f"{current_path}/image"


# 传入一段文字，返回一个图片
def get_image(text:str, user_id:str) -> str:
    # 设置字体大小
    font_size = 20

    # 以\n分割text，获取行数，根据行数设置图片高度，获取分割后最长的一行的长度，设置图片宽度
    text_lines = text.split('\n')
    text_height = len(text_lines) * font_size * 1.3
    text_width = max([len(line) for line in text_lines]) * font_size


    # 创建一个新图片
    image = Image.new('RGB', (int(text_width), int(text_height)), (255, 255, 255))
    # 创建一个画笔
    draw = ImageDraw.Draw(image)
    # 设置字体
    font = ImageFont.truetype(font_path, size=font_size)
    # 绘制文字
    draw.text((10, 10), text, (0, 0, 0), font=font)
    # 保存图片
    image.save(f"{save_path}/{user_id}.png")
    return f"{save_path}/{user_id}.png"


# 传入一段文字，返回一个图片
def get_image_by_admin(texta:str, textb:str) -> str:
    # 设置字体大小
    font_size = 19
    # 创建一个新图片
    image = Image.new('RGB', (1000, 1000), (255, 255, 255))
    # 创建一个画笔
    draw = ImageDraw.Draw(image)
    # 设置字体
    font = ImageFont.truetype(f"{current_path}/data/yuanshen.ttf", size=font_size)
    # 绘制文字
    draw.text((30, 10), texta, (0, 0, 0), font=font)



    # 设置字体大小
    font_size = 20
    # 设置字体
    font = ImageFont.truetype(f"{current_path}/data/consola-1.ttf", size=font_size)
    # 绘制文字
    draw.text((180, 30), textb, (0, 0, 0), font=font)



    # 保存图片
    image.save(f"{save_path}/shop.png")
    return f"{save_path}/shop.png"