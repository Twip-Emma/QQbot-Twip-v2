'''
Author: 七画一只妖
Date: 2022-01-23 10:47:20
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 13:57:18
Description: file content
'''
import MySQLdb
from PIL import Image
import base64
from io import BytesIO


from tool.setting.database_setting import *
from .get_image_new import data_to_image


# 查出指定用户的所有信息
def find_user_info(user_id: str) -> list:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM user_info WHERE user_id=" + user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    return results[0]


# 图片转b64
def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


# 主控
def start(user_id: str) -> str:
    user_info = find_user_info(user_id)
    return data_to_image(user_info)

