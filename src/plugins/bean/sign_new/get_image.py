'''
Author: 七画一只妖
Date: 2021-11-24 14:58:57
LastEditors: 七画一只妖
LastEditTime: 2021-11-24 21:15:33
Description: file content
'''
from PIL import Image, ImageDraw, ImageFont
import json
import time
import random
import datetime
import os
from os import path

FILE_PATH = path.join(path.dirname(__file__))

TRA = {
    "whisper of autunmn":"秋天的低语",
    "feather wave":"羽毛 波",
    "time to journey":"旅行时间",
    "fam al-fut":"我们快饿死了",
    "东陵红渊":"东陵红渊",
    "forces of the sky":"天空的力量",
    "present = past + future":"现在=过去+未来",
    "mid sense melancholy":"中感忧郁",
    "望乡~departure":"望乡~离开",
    "memories of a town":"乡村记忆",
    "":"",
    "":"",
}

SIGN_IMG = ["冲虚","低语","高歌","救苦","普渡","深渊","万神","往生","智慧","自在"]
    

def get_bg(luck_name):
    bg = Image.open(f"{FILE_PATH}\\icon\\背景.png")
    luck_img = Image.open(f"{FILE_PATH}\\icon\\{luck_name}.png")

    luck_size = 0.7 # 定义图标缩放尺寸
    luck_img = luck_img.resize((int(luck_img.width * luck_size),int(luck_img.height * luck_size)))

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
def write_something(bg_img,text,verse, user_name, time, chaos_num):
    text = text[0] + "   " + text[1]

    # font_path = os.path.join(f"{FILE_PATH}\\ttf\\印章繁体方篆.ttf")
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 60  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(680))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = text.replace("   "," ")
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\印章繁体方篆.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(740))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    verse = verse.replace("，","     ")
    text = f"{verse}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 36  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(800))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"信徒 ： {user_name}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(850))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"Chaos :  {chaos_num}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 30  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(890))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字
    
    text = f"时间 ： {time}"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\华文新魏.ttf")
    font_size = 25  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(930))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"--  Synthèse d'images : Twip  --"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 25  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(960))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字

    text = f"-- Le vent glacial ne s'est pas adapté, les oiseaux chantent sur la rive --"
    font_path = os.path.join(f"{FILE_PATH}\\ttf\\Snell-Roundhand字体.ttf")
    font_size = 40  # 定义字体大小
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text=text)
    draw = ImageDraw.Draw(bg_img)
    text_coordinate = (int((bg_img.width - text_width[0])/2), int(1000))  # 要写字的地方
    draw.text(text_coordinate, text, fill="#e4e6b5", font=font)  # 正式写字
    
    
    # Synthèse d'images
    # bg_img.show()
    return bg_img

# logo = SIGN_IMG[9]

# 主控
# 传入参数：
def start(logo_name, verse, user_name, time, chaos_num):
    bg_img = get_bg(logo_name)
    re = write_something(bg_img,logo_name,verse, user_name, time, chaos_num)
    return re


# a = "123123，12313，1231312"
# a = a.replace("，", "x")
# print(a)