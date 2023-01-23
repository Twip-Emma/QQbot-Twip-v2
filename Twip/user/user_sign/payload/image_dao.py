'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-12-09 09:17:23
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-12-10 10:40:25
'''
import datetime
import random
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont, ImageMath

from .data.pray_txt import PARY_TABLE
from .data_handler import change_sign_info, insert_new_user, select_user
from .image_factory import FontEntity, picture_paste_img, write_longsh

BASE_PATH: str = Path(__file__).absolute().parents[0]


# qq头像接口
QQ_API1 = "http://q1.qlogo.cn/g?b=qq&nk=|QQ号码|&s=640"

# qq群头像接口
QQ_API2 = "http://p.qlogo.cn/gh/|QQ群号码|/|QQ群号码|/100/"


# 获取头像
def get_user_image(user_id: str) -> Image:
    # 图片url转bytes
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    res = requests.get(url)
    byte_stream = BytesIO(res.content)
    return Image.open(byte_stream)


# 获取运势
def get_lucky(user_id:str) -> str:
    user = select_user(user_id)
    if user == []: # 判断为新用户
        info = get_luck_info()
        insert_new_user(user_id, info)
        return info
    else:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if user[0][1] == now_time: # 今日已签到
            return user[0][2]
        else: # 今日首次签到
            info = get_luck_info()
            change_sign_info(user_id, info)
            return info


# 获取运势信息
def get_luck_info() -> str:
    info = None
    luck_num = random.randint(1,1000)
    print(luck_num)

    flag = random.randint(1,100)
    if flag <= 50:
        if luck_num <= 30:
            luck_num2 = random.randint(100000,10000000)
            info = "大吉|" + random.choice(PARY_TABLE["大吉"]) + "|" + str(luck_num2) + "|繁     锦|A"
        elif luck_num <= 100:
            luck_num2 = random.randint(1000,99999)
            info = "中吉|" + random.choice(PARY_TABLE["中吉"]) + "|" + str(luck_num2) + "|争     妍|A"
        elif luck_num <= 300:
            luck_num2 = random.randint(10,999)
            info = "小吉|" + random.choice(PARY_TABLE["小吉"]) + "|" + str(luck_num2) + "|归     鸟|A"
        elif luck_num <= 1000:
            luck_num2 = random.randint(0,9)
            info = "末吉|" + random.choice(PARY_TABLE["末吉"]) + "|" + str(luck_num2) + "|疏     影|A"
        else:
            luck_num2 = random.randint(100000,10000000)
            info = "大吉|" + random.choice(PARY_TABLE["大吉"]) + "|" + str(luck_num2) + "|繁     锦|A"
        return info
    else:
        if luck_num <= 30:
            luck_num2 = random.randint(100000,10000000)
            info = "大吉|" + random.choice(PARY_TABLE["大吉"]) + "|" + str(luck_num2) + "|渺 镜 云 烟|B"
        elif luck_num <= 100:
            luck_num2 = random.randint(1000,99999)
            info = "中吉|" + random.choice(PARY_TABLE["中吉"]) + "|" + str(luck_num2) + "|纯 白 之 心|B"
        elif luck_num <= 300:
            luck_num2 = random.randint(10,999)
            info = "小吉|" + random.choice(PARY_TABLE["小吉"]) + "|" + str(luck_num2) + "|诸 坠 渊 若|B"
        elif luck_num <= 1000:
            luck_num2 = random.randint(0,9)
            info = "末吉|" + random.choice(PARY_TABLE["末吉"]) + "|" + str(luck_num2) + "|惄 焉 伤 悴|B"
        else:
            luck_num2 = random.randint(100000,10000000)
            info = "大吉|" + random.choice(PARY_TABLE["大吉"]) + "|" + str(luck_num2) + "|渺 镜 云 烟|B"
        return info


# 制作背景总控
def make_bg(user_id:str, user_name: str) -> Image:
    user_head = get_user_image(user_id)
    user_head = user_head.resize((300,300))


    info = get_lucky(user_id)
    info = info.split("|")

    # 判断运势类型
    if info[4] == "A":
        bg = Image.open(Path(BASE_PATH)/r"image"/r"BaseBG.png")
        location = int((bg.width - user_head.width)/2), 150
        a1 = picture_paste_img(user_head, bg, location)
        a2 = picture_paste_img(Image.open(Path(BASE_PATH)/r"image"/r"BaseBG3.png"), a1)

        # 写什么运势
        ft = FontEntity(fsize=100, color="#FF99FF")
        a3 = write_longsh(ft, a2, info[3], "C", (450,0))
        ft.setColor("#FF66FF").setSize(35)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        a4 = write_longsh(ft, a3, f"幸运度：{info[2]}\n\n{user_name}   {now_time}", "C", (600,0))
        ft.setColor("#9933CC").setSize(25)
        a5 = write_longsh(ft, a4, f"密语", "C", (730,0))

        # 写密语
        ft.setTTF(Path(BASE_PATH)/r"ttf"/r"七画体b3.otf").setSize(30).setColor("#660099")
        txt = info[1].replace("-","\n\n")
        a6 = write_longsh(ft, a5, txt, "C", (780,0))

        # 选择猫猫
        luck = info[0]
        luck = luck.replace(" ","")
        neko = Image.open(Path(BASE_PATH)/r"image"/f"{luck}.png")
        neko = neko.resize((int(neko.width * 0.5), int(neko.height * 0.5)))
        a7 = picture_paste_img(neko, a6, (200, 600))
        a8 = picture_paste_img(Image.open(Path(BASE_PATH)/r"image"/r"cover.png"), a7)

        # 保存图片
        save_path = str(Path(BASE_PATH)/r"cache"/f"{user_id}.jpg")
        a8 = a8.convert("RGB")
        a8.save(save_path)
    else:
        bg = Image.open(Path(BASE_PATH)/r"image"/r"BaseBG4.png")
        location = int((bg.width - user_head.width)/2), 150
        a1 = picture_paste_img(user_head, bg, location)
        a2 = picture_paste_img(Image.open(Path(BASE_PATH)/r"image"/r"BaseBG5.png"), a1)
        
        # 写什么运势
        ft = FontEntity(fsize=100, color="#0099FF")
        a3 = write_longsh(ft, a2, info[3], "C", (480,0))
        ft.setColor("#3399FF").setSize(35)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        a4 = write_longsh(ft, a3, f"幸运度：{info[2]}\n\n{user_name}   {now_time}", "C", (600,0))
        ft.setColor("#0066CC").setSize(25)
        a5 = write_longsh(ft, a4, f"密语", "C", (730,0))

        # 写密语
        ft.setTTF(Path(BASE_PATH)/r"ttf"/r"七画体b3.otf").setSize(30).setColor("#3333FF")
        txt = info[1].replace("-","\n\n")
        a6 = write_longsh(ft, a5, txt, "C", (780,0))

        a6 = picture_paste_img(Image.open(Path(BASE_PATH)/r"image"/r"cover2.png"), a6)

        # 保存图片
        save_path = str(Path(BASE_PATH)/r"cache"/f"{user_id}.jpg")
        a6 = a6.convert("RGB")
        a6.save(save_path)

    return save_path