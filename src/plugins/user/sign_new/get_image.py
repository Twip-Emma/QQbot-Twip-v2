'''
Author: 七画一只妖
Date: 2021-11-24 14:58:57
LastEditors: 七画一只妖
LastEditTime: 2022-07-26 12:57:29
Description: file content
'''
from PIL import Image, ImageDraw, ImageFont
import os
from os import path

FILE_PATH = path.join(path.dirname(__file__))



SIGN_IMG = ["冲虚", "低语", "高歌", "救苦", "普渡", "深渊", "万神", "往生", "智慧", "自在"]


def get_bg(luck_name):
    bg = Image.open(f"{FILE_PATH}\\icon\\背景.png")
    bg.convert("RGB")
    luck_img = Image.open(f"{FILE_PATH}\\icon\\{luck_name}.png")
    luck_img.convert("RGB")
    luck_img.resize((500,500))

    if luck_name in SIGN_IMG:
        luck_size = 0.7  # 定义图标缩放尺寸
        luck_img = luck_img.resize(
            (int(luck_img.width * luck_size), int(luck_img.height * luck_size)))

    bg_x = bg.width
    bg_y = bg.height
    ly_x = luck_img.width
    ly_y = luck_img.height

    # 计算坐标
    add = (int((bg_x - ly_x)/2), int((bg_y - ly_y)/2))

    bg.paste(luck_img, add, luck_img)
    # bg.show()
    return bg


# 写字
def write_something(bg_img, text, verse, user_name, time, chaos_num) -> Image:
    text = "   ".join(text)

    # font_path = os.path.join(f"{FILE_PATH}\\ttf\\印章繁体方篆.ttf")
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 60  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(680))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = text.replace("   ", " ")
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\印章繁体方篆.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(740))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    verse = verse.replace("，", "     ")
    text = f"{verse}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 36  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(800))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"信徒 ： {user_name}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(850))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"Chaos :  {chaos_num}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(890))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"时间 ： {time}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 25  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(930))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"--  Synthèse d'images : Twip  --"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 25  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(960))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"-- Le vent glacial ne s'est pas adapté, les oiseaux chantent sur la rive --"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 40  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (
        int((bg_img.width - text_width[0])/2), int(1000))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    # Synthèse d'images
    # bg_img.show()

    # 缩小图片尺寸
    # bg_img = smaller_pic(bg_img)
    return bg_img

# logo = SIGN_IMG[9]

# 主控
# 传入参数：


def start(logo_name, verse, user_name, time, chaos_num):
    bg_img = get_bg(logo_name)
    re = write_something(bg_img, logo_name, verse, user_name, time, chaos_num)
    return re


def smaller_pic(image: Image) -> Image:
    ly_x = image.width * 0.3
    ly_y = image.height * 0.3
    image = image.resize(int(ly_x), int(ly_y))
    return image

# a = "123123，12313，1231312"
# a = a.replace("，", "x")
# print(a)
