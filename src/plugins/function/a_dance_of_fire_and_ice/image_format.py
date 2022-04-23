'''
Author: 七画一只妖
Date: 2022-04-22 21:53:24
LastEditors: 七画一只妖
LastEditTime: 2022-04-23 13:30:12
Description: file content
'''
from io import BytesIO
from os import path
from PIL import Image, ImageDraw, ImageFont
FILE_PATH = path.join(path.dirname(__file__))


# 将传入的文字转图片
async def text_to_pic(text: str) -> str:
    bg = Image.new("RGB", (600, 1500), (255, 255, 255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\zh-cn.ttf", 15)
    dr.text((10, 5), text=text, font=font, fill="#000000")
    
    # 保存图片到\data内，命名为all_song.jpg
    bg.save(f"{FILE_PATH}\\data\\all_song.jpg")
    return f"{FILE_PATH}\\data\\all_song.jpg"