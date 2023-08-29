'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-12-09 09:17:23
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 13:52:24
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
def get_luck_info():
    info = None
    luck_num = random.randint(1,1000)

    if luck_num <= 10:
        luck_num2 = -99999999
        info = '地狱'
    elif luck_num <= 30:
        luck_num2 = random.randint(100000,10000000)
        info = random.choice(PARY_TABLE["大吉"])
    elif luck_num <= 100:
        luck_num2 = random.randint(1000,99999)
        info = random.choice(PARY_TABLE["中吉"])
    elif luck_num <= 300:
        luck_num2 = random.randint(10,999)
        info = random.choice(PARY_TABLE["小吉"])
    elif luck_num <= 1000:
        luck_num2 = random.randint(0,9)
        info = random.choice(PARY_TABLE["末吉"])
    else:
        luck_num2 = random.randint(100000,10000000)
        info = random.choice(PARY_TABLE["大吉"])
    return f"{info}|{luck_num2}"


# 制作背景总控
def make_bg(user_id:str, user_name: str) -> Image:
    info = get_lucky(user_id).split("|")


    # 写什么幸运度和昵称
    ft = FontEntity(fsize=100, color="#00BFFF")
    a2 = Image.open(Path(BASE_PATH)/r"image"/fr"{info[0]}.png")
    a3 = write_longsh(ft, a2, info[0], "C", (1000,0))
    ft.setColor("#00FFFF").setSize(35)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    a4 = write_longsh(ft, a3, f"幸运度：{info[1]}\n\n{user_name}   {now_time}", "C", (1150,0))


    # 保存图片
    save_path = str(Path(BASE_PATH)/r"cache"/f"{user_id[0]}.jpg")
    a4 = a4.convert("RGB")
    a4.save(save_path)

    return save_path