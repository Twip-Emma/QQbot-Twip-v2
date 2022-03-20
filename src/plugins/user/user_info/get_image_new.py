'''
Author: 七画一只妖
Date: 2022-03-20 13:02:37
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 13:50:16
Description: file content
'''
import base64
from io import BytesIO
from os import path

from PIL import Image, ImageDraw, ImageFont


FILE_PATH = path.join(path.dirname(__file__))

IMAGE_PATH = f"{FILE_PATH}\\image\\user_info.png"


# 将数据转成图片返回图片路径
def data_to_image(data: list) -> str:
    text = ""

    text += "亲爱的" + str(data[0]) + "(" + str(data[1]) + ")" + "，您好！\n\n"
    text += "你的总发言：" + str(data[4]) + "次\n\n"
    text += "你的总金币：" + str("%.2f" % data[5]) + "个\n\n"
    text += "你的收集品：" + "--%" + "\n\n"

    bg = Image.new("RGB", (400, 300), (255, 255, 255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\zh-cn.ttf", 20)

    dr.text((10, 5), text=text, font=font, fill="#000000")

    # 保存图片到image文件夹

    bg.save(IMAGE_PATH)

    return IMAGE_PATH

