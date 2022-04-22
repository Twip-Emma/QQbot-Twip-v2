'''
Author: 七画一只妖
Date: 2022-04-22 21:53:24
LastEditors: 七画一只妖
LastEditTime: 2022-04-22 22:05:46
Description: file content
'''
from io import BytesIO
from os import path
from PIL import Image, ImageDraw, ImageFont
FILE_PATH = path.join(path.dirname(__file__))


# 将传入的文字转图片
async def text_to_pic(text: str) -> bytes:
    bg = Image.new("RGB", (1000, 1000), (255, 255, 255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\zh-cn.ttf", 15)
    dr.text((10, 5), text=text, font=font, fill="#000000")
    
    # 转bytes
    img_bytes = BytesIO()
    bg.save(img_bytes, format="png")
    img_bytes.seek(0)
    return img_bytes.read()