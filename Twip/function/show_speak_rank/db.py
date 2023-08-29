'''
Author: 七画一只妖
Date: 2022-03-01 20:27:54
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 14:09:10
Description: file content
'''

import base64
from io import BytesIO
import time
from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB, TTF_PATH
import MySQLdb
from os import path

from PIL import Image, ImageDraw, ImageFont

FILE_PATH = path.join(path.dirname(__file__))


# 设定一个时间 2021年1月20日
OLD_TIME = time.strptime("2021-01-20 00:00:00", "%Y-%m-%d %H:%M:%S")


# 获取现在的时间
def get_now_time() -> str:
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return now_time


def find_speak_rank() -> list:
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    sql = "select * from user_info order by speak_time_total desc limit 0,99;"
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


# 将数据转成图片返回image对象
def data_to_image(data,type:str) -> str:
    # 获取当前时间
    now_time = get_now_time()
    # 获取时间差
    time_difference = time.mktime(time.strptime(now_time, "%Y-%m-%d %H:%M:%S")) - time.mktime(OLD_TIME)
    # 将时间差转换
    day =int( time_difference // (24 * 60 * 60))
    hour = int((time_difference - day * 24 * 60 * 60) // (60 * 60))
    minute = int((time_difference - day * 24 * 60 * 60 - hour * 60 * 60) // 60)
    second = int(time_difference - day * 24 * 60 * 60 - hour * 60 * 60 - minute * 60)
    time_difference = f"{day} 天 {hour} 小时 {minute} 分 {second} 秒"



    ################################################
    text1 = ""
    rank = 1
    for item in data:
        # user_item = f"【{str(rank)}】{item[0]}({item[1]})的发言次数是：{item[4]}\n\n"
        # 对齐
        user_item = f"[{str(rank):>2}] ===> {item[4]:>6}   |\n\n"
        text1 += user_item
        rank += 1
    bg = Image.new("RGB",(650,5000), (255,255,255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\consola-1.ttf", 20)
    dr.text((10,100), text=text1, font=font, fill="#000000")
    ################################################
    text2 = ""
    rank = 1
    for item in data:
        # user_item = f"【{str(rank)}】{item[0]}({item[1]})的发言次数是：{item[4]}\n\n"
        # 对齐
        # item[1]是一个字符串，将这个字符串的开头两个字符和结尾两个字符换成*号
        if type == "admin":
            user_item = f"{item[0]} ( {item[1]} ) \n\n"
        else:
            user_item = f"{item[0]} ( {item[1][:4]}{'*'*(len(item[1])-4)} ) \n\n"
        # user_item = f"{item[0]} ( {item[1]} ) \n\n"
        text2 += user_item
        rank += 1
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(TTF_PATH, 19)
    dr.text((275,100), text=text2, font=font, fill="#000000")
    ################################################
    text3 = f"当前时间：{now_time}\n\n"
    text4 = f"统计时长：{time_difference}\n\n"
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(TTF_PATH, 19)
    # 将text3和text4居中
    text_width3 = font.getsize(text=text3)
    text_width4 = font.getsize(text=text4)
    text_width5 = font.getsize(text="By  Twip  七画一只妖")
    dr.text(((650-text_width3[0])/2,20), text=text3, font=font, fill="#000000")
    dr.text(((650-text_width4[0])/2,20+text_width3[1]), text=text4, font=font, fill="#000000")
    dr.text(((650-text_width5[0])/2,20+text_width3[1]+text_width4[1]), text="By  Twip  七画一只妖", font=font, fill="#000000")

    # bg.show()
    return img_to_b64(bg)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str