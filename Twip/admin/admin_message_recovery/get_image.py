'''
Author: 七画一只妖
Date: 2022-03-12 22:37:57
LastEditors: 七画一只妖
LastEditTime: 2022-03-13 10:18:17
Description: file content
'''
import base64
from io import BytesIO
from os import path

from PIL import Image, ImageDraw, ImageFont
from .database_config import *


FILE_PATH = path.join(path.dirname(__file__))


# 将数据转成图片返回image对象
def data_to_image(data:list) -> str:
    text = ""
    bg_height = int(len(data) * 40)
    for item in data:
        user_item = f"{item}\n\n"
        text += user_item

    bg = Image.new("RGB",(650,bg_height), (255,255,255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\yuanshen.ttf", 15)

    dr.text((10,5), text=text, font=font, fill="#000000")

    # bg.show()
    return img_to_b64(bg)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


def start(group_id:str, count:str):
    message_list = get_message_by_time_limit(group_id=group_id,count=count)
    message_user_list = []
    for message in message_list:
        context = message[2]
        if "CQ:image" in context:
            context = "[图片]"
        speak_time = message[5]
        user_name = get_name_by_id(message[4])

        total_speak = f"【{user_name}】{context}({speak_time})"
        message_user_list.append(total_speak)
    return data_to_image(message_user_list)
