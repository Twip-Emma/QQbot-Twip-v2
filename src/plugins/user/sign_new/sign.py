'''
Author: 七画一只妖
Date: 2021-11-24 14:29:43
LastEditors: 七画一只妖
LastEditTime: 2022-03-28 22:29:41
Description: file content
'''

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import time
import random
import datetime
import base64
from os import path
import os

FILE_PATH = path.join(path.dirname(__file__))

from .get_image import start


THIS_PATH = path.join(path.dirname(__file__))
SIGN_CHACK_PATH = f"{THIS_PATH}\\user_sign.json"
SIGN_INFO_PATH = f"{THIS_PATH}\\sign_info.json"


def check_user_sign(user_id,user_name) -> Image:
    now_time = time.strftime('%Y %m %d', time.localtime(time.time()))
    data:dict = json.load(open(SIGN_CHACK_PATH, 'r', encoding='utf8'))
    luck_num = random.randint(1,1000)
    
    img = "出错了"
    if user_id not in data:
        luck_info = find_luck_info(luck_num,user_name)
        new_obj = {user_id:{
            "user_id":user_id,
            "now_time":now_time,
            "luck_info":luck_info
        }}
        img = get_image_by_cq(luck_info,user_id)
        data.update(new_obj)
    else:
        if data[user_id]["now_time"] == now_time:
            img = get_image_by_cq(data[user_id]["luck_info"],user_id)
        else:
            data[user_id]["now_time"] = now_time
            luck_info = find_luck_info(luck_num,user_name)
            img = get_image_by_cq(luck_info,user_id)

    with open(SIGN_CHACK_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()

    return img


def find_luck_info(num,user_name):
    data:dict = json.load(open(SIGN_INFO_PATH, 'r', encoding='utf8'))
    if num <= 50:
        tag = "S"
    elif num <=150:
        tag = "L"
    elif num <= 400:
        tag = "F"
    elif num <= 500:
        tag = "M"
    else:
        tag = "R"

    # 选择logo
    if tag == "S":
        luck_ing = random.choice(["普渡","万神","与愿"])
    elif tag == "L":
        luck_ing = random.choice(["高歌","救苦","莫测","守序"])
    elif tag == "F":
        luck_ing = random.choice(["深渊","低语","堕入三恶道","因果报应"])
    elif tag == "M":
        luck_ing = random.choice(["往生","冲虚","人间万事非","再受业报"])
    elif tag == "R":
        luck_ing = random.choice(["自在","智慧","何处染尘埃","身是菩提树"])

    # 选择诗句
    verse = random.choice(data["verse"][tag])

    # 生成时间
    now_time = time.strftime('%Y 年 %m 月 %d 日', time.localtime(time.time()))

    # 生成乱数
    if tag == "S":
        chaos_num = str(random.randint(10000,99999))
    elif tag == "L":
        chaos_num = str("?0." + str(random.randint(100,999)))
    elif tag == "F":
        chaos_num = str("-" + str(random.randint(10000,99999)))
    elif tag == "M":
        chaos_num = str("-0." + str(random.randint(100,999)))
    elif tag == "R":
        chaos_num = str(random.randint(1,10))

    user_luck_info = {
        "user_name":user_name,
        "luck_ing":luck_ing,
        "verse":verse,
        "now_time":now_time,
        "chaos_num":chaos_num
    }
    return user_luck_info


def get_image_by_cq(user_info:dict,user_id):
    user_name = user_info["user_name"]
    luck_ing = user_info["luck_ing"]
    verse = user_info["verse"]
    now_time = user_info["now_time"]
    chaos_num = user_info["chaos_num"]
    img = start(luck_ing, verse, user_name, now_time, chaos_num)
    # b64 = pic2b64(img)
    # cq = ba64_to_cq(b64)
    
    # 返回图片保存的路径
    pic_path = save_image(img,user_id)
    img = Image.open(pic_path)

    return img

# 把传进来的Image对象转成base64
def pic2b64(im:Image):
    im = im.resize((int(im.width * 0.7),int(im.height * 0.7)))
    bio = BytesIO()
    im.save(bio, format='PNG')
    base64_str = base64.b64encode(bio.getvalue()).decode()
    return 'base64://' + base64_str


# 转CQ码
def ba64_to_cq(base64_str):
    return f"[CQ:image,file={base64_str}]"


# 保存图片，返回路径
def save_image(img,userid):
    img_path = os.path.join(f'{FILE_PATH}\\image\\{userid}.jpg')
    # 保存图片
    bg_finally = img.convert("RGB")
    bg_finally.save(img_path)
    cq = f"{FILE_PATH}\\image\\{userid}.jpg"
    return cq