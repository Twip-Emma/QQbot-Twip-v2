'''
Author: 七画一只妖
Date: 2022-01-07 20:43:34
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 13:16:09
Description: file content
'''
import base64
from io import BytesIO

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.typing import T_State

from PIL import Image

from tool.find_power.format_data import is_level_S
from .logo import make_logo

phlogo = on_command("phlogo", aliases={"pornhub", "ph图标"})


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


@phlogo.handle()
async def _(bot: Bot, event: MessageEvent):
    if not is_level_S(event):
        phlogo.finish()
    msg = str(event.get_message()).split()
    if len(msg) == 3:
        pic = img_to_b64(make_logo(msg[1], msg[2]))
        await phlogo.finish(MessageSegment.image(pic))
    else:
        await phlogo.finish("请输入正确的参数,用空格分开")
