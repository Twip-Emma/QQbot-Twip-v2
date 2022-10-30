'''
Author: 七画一只妖
Date: 2021-11-24 14:58:57
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-30 22:12:41
Description: file content
'''
from PIL import Image, ImageDraw, ImageFont
import os

from Twip import ABSOLUTE_PATH

FILE_PATH = f"{ABSOLUTE_PATH}\\user\\sign_new"


def get_bg(luck_name):
    bg = Image.open(f"{FILE_PATH}\\icon\\背景.png").convert("RGBA")
    luck_img = Image.open(f"{FILE_PATH}\\icon\\{luck_name}.png").convert("RGBA")
    luck_img = luck_img.resize((300,300))

    # 计算坐标
    add = (int((bg.width - luck_img.width)/2), int((bg.height - luck_img.height)/2))

    bg.paste(luck_img, add, luck_img)
    return bg


# 写字
def write_something(bg_img, text, verse, user_name, time, chaos_num) -> Image:
    ttf_list = ["华文新魏","印章繁体方篆","华文新魏","华文新魏","Snell-Roundhand字体","华文新魏"]
    fsize_lsit = [60,30,36,30,30,25]
    text_list = []
    text = "   ".join(text)
    text_list.append(text)
    text_list.append(text.replace("   ", " "))
    text_list.append(verse.replace("，", "     "))
    text_list.append("信徒 : " + user_name)
    text_list.append("Chaos :  " + chaos_num)
    text_list.append("时间 :  " + time)
    location_list = [680,740,800,850,890,930]

    for i in range(0, 6):
        # 生成字体：字体路径、字体大小
        font = ImageFont.truetype(os.path.join(FILE_PATH + "\\ttf\\" + ttf_list[i] +".ttf"), fsize_lsit[i])
        text_width = font.getsize(text=text_list[i]) # 获取文本长度
        draw = ImageDraw.Draw(bg_img)
        text_coordinate = (
            int((bg_img.width - text_width[0])/2), location_list[i])  # 要写字的地方
        draw.text(text_coordinate, text_list[i], fill="#e4e6b5", font=font)  # 正式写字

    return bg_img


def start(logo_name, verse, user_name, time, chaos_num):
    bg_img = get_bg(logo_name)
    re = write_something(bg_img, logo_name, verse, user_name, time, chaos_num)
    return re