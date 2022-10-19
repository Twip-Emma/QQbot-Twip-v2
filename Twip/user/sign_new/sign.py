'''
Author: 七画一只妖
Date: 2021-11-24 14:29:43
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-18 19:40:55
Description: file content
'''

import datetime
import time
import random
import os

from Twip import ABSOLUTE_PATH
FILE_PATH = f"{ABSOLUTE_PATH}\\user\\sign_new"

from .user_get_test import SIGN_TEXT
from .user_sql import select_user, insert_new_user, change_sign_info
from .get_image import start as image_start


# 求签主函数，由init调用
def user_sign_main(user_id:str, user_name) -> str:
    
    luck_num = random.randint(1,1000)
    user = select_user(user_id)

    if user == []: # 判断为新用户
        info = find_luck_info(luck_num, user_name)
        insert_new_user(user_id, info)
        return get_image_by_cq(info, user_id)
    else:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if user[0][1] == now_time: # 今日已签到
            return get_image_by_cq(user[0][2], user_id)
        else: # 今日首次签到
            info = find_luck_info(luck_num, user_name)
            change_sign_info(user_id, info)
            return get_image_by_cq(info,user_id)


def find_luck_info(num,user_name) -> str:
    data:dict = SIGN_TEXT
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

    return f"""{user_name}|+twip+|{luck_ing}|+twip+|{verse}|+twip+|{now_time}|+twip+|{chaos_num}"""


def get_image_by_cq(user_info:str, user_id:str) -> str:
    user_info_list = user_info.split("|+twip+|")
    user_name = user_info_list[0]
    luck_ing = user_info_list[1]
    verse = user_info_list[2]
    now_time = user_info_list[3]
    chaos_num = user_info_list[4]
    img = image_start(luck_ing, verse, user_name, now_time, chaos_num)
    
    # 返回图片保存的路径
    pic_path = save_image(img,user_id)

    return pic_path
    

# 把传进来的Image对象转成base64
# def pic2b64(im:Image):
#     im = im.resize((int(im.width * 0.7),int(im.height * 0.7)))
#     bio = BytesIO()
#     im.save(bio, format='PNG')
#     base64_str = base64.b64encode(bio.getvalue()).decode()
#     return 'base64://' + base64_str


# # 转CQ码
# def ba64_to_cq(base64_str):
#     return f"[CQ:image,file={base64_str}]"


# 保存图片，返回路径
def save_image(img,userid):
    img_path = os.path.join(f'{FILE_PATH}\\image\\{userid}.jpg')
    # 保存图片
    bg_finally = img.convert("RGB")
    bg_finally.save(img_path)
    cq = f"file:///{FILE_PATH}/image/{userid}.jpg"
    return cq