'''
Author: 七画一只妖
Date: 2022-01-23 10:47:11
LastEditors: 七画一只妖
LastEditTime: 2022-03-01 21:01:05
Description: file content
'''
'''
Author: 七画一只妖
Date: 2021-11-24 14:58:57
LastEditors: 七画一只妖
LastEditTime: 2022-01-19 19:44:54
Description: file content
'''

from PIL import Image, ImageDraw, ImageFont
import json
import time
import random
import datetime
import os
from os import path

from sqlalchemy import null
FILE_PATH = path.join(path.dirname(__file__))


# 对背景图像进行调整
def get_bg():
    luck_img = Image.open(f"{FILE_PATH}\\icon\\user_info_bg_1.png")
    luck_img.convert("RGB")

    # luck_size = 0.7  # 定义图标缩放尺寸
    # luck_img = luck_img.resize(
    #     (int(luck_img.width * luck_size), int(luck_img.height * luck_size)))

    return luck_img


# 写字
def write_something(bg_img: Image, user_name: str, user_id: str, user_level: str, speak_total, coin_total) -> Image:
    # Snell-Roundhand字体 华文新魏 HappyBirthday

    text = "PASS COMMON"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 80  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(450))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"{user_name}<{user_id}>"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 60  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(600))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"活跃等级"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(300), int(750))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    text = f"发言次数："
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(300), int(850))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    text = f"剩余货币："
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(300), int(950))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    text = f"null"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(700), int(750))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    text = f"{speak_total}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(700), int(850))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    text = f"{coin_total}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 50  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int(700), int(950))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#000000", font=font)  # 正式写字

    # bg_img.show()
    path = save_image(bg_img,user_id)
    img = Image.open(path)

    return img


# 保存图片，返回路径
def save_image(img,userid):
    img_path = os.path.join(f'{FILE_PATH}\\image\\{userid}.jpg')
    # 保存图片
    bg_finally = img.convert("RGB")
    bg_finally.save(img_path)
    cq = f"{FILE_PATH}\\image\\{userid}.jpg"
    return cq


# 主控
def get_image_start(user_name:str, user_id:str, user_level:str, speak_total:str, coin_total:str):
    bg = get_bg()
    img = write_something(bg, user_name, user_id, user_level, speak_total, coin_total)
    return img
