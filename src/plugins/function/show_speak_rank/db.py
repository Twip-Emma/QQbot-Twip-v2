'''
Author: 七画一只妖
Date: 2022-03-01 20:27:54
LastEditors: 七画一只妖
LastEditTime: 2022-03-01 20:55:08
Description: file content
'''

import base64
from io import BytesIO
from tool.setting.database_setting import *
import MySQLdb
from os import path

from PIL import Image, ImageDraw, ImageFont

FILE_PATH = path.join(path.dirname(__file__))

def find_speak_rank() -> list:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    sql = "select * from user_info order by speak_time_total desc limit 0,100;"
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


# 将数据转成图片返回image对象
def data_to_image(data) -> str:
    text = ""
    rank = 1
    for item in data:
        user_item = f"【{str(rank)}】{item[0]}({item[1]})的发言次数是：{item[4]}\n\n"
        text += user_item
        rank += 1

    bg = Image.new("RGB",(650,5000), (255,255,255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\yuanshen.ttf", 20)

    dr.text((10,5), text=text, font=font, fill="#000000")

    # bg.show()
    return img_to_b64(bg)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str