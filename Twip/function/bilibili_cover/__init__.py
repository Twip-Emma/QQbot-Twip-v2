'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-06-04 13:13:19
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-06-04 13:16:24
FilePath: \QQbot-Twip-v2\Twip\function\bilibili_cover\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import re
from pathlib import Path

import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
import requests

from tool.find_power.format_data import is_level_S


get_img = on_command("封面", block=True, priority=1)


@get_img.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    msg = str(event.get_message()).split()

    if len(msg) == 1:
        await get_img.finish("请在指令后面加空格加BV号")

    await get_img.send(MessageSegment.image(await extract_bilibili_cover(msg[1])))


async def extract_bilibili_cover(bv: str):
    # 发送请求获取视频封面链接
    async with httpx.AsyncClient(timeout=None, follow_redirects=True) as client:
        response = await client.get(f"https://www.strerr.com/gentle-block-5b16/?b={bv}")
        img_url = response.json()["url"]["url"]
    # 保存到本地
    return img_url