'''
Author: 七画一只妖
Date: 2022-03-14 22:37:35
LastEditors: 七画一只妖
LastEditTime: 2022-03-14 23:07:33
Description: file content
'''
import base64
from io import BytesIO
from tool.find_power.format_data import is_level_S
import MySQLdb
from os import path
import requests

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

from PIL import Image


BASE_URL = "http://pixiv.re/"


def get_image_from_url(pid:str) -> Image.Image:
    image_url = f"{BASE_URL}{pid}.png"
    resp = requests.get(url=image_url, allow_redirects=False)
    image = Image.open(BytesIO(resp.content))
    return image


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


# 根据url获取图片
def get_image_from_url2(url: str) -> Image.Image:
    resp = requests.get(url=url, allow_redirects=False)
    image = Image.open(BytesIO(resp.content))
    return image


# 主控函数
def start(pid:str):
    # 获取图片
    image = get_image_from_url(pid)
    # 判断图片是否有效
    try:
        base64_str = img_to_b64(image)
        # 发送图片
        return base64_str
    except:
        return None


get_pic = on_command("搜索图片")

@get_pic.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await get_pic.finish()
    pid = event.message.extract_plain_text().split(" ")[1]
    re = start(pid)
    if re:
        await get_pic.send(MessageSegment.image(re))
    else:
        await get_pic.send("图片无效")