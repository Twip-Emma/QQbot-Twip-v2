'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:01:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-04-01 14:43:39
FilePath: \060坎公骑冠剑会战工具\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import re
from pathlib import Path

import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
import requests

from tool.find_power.format_data import is_level_A

from .payload.dao import get_data, get_data_total, get_rate

BASE_PATH: str = Path(__file__).absolute().parents[0]
pattern = re.compile(r"url=(.*?)&amp;")


daily = on_command("战报", aliases={"每日战报", "每日", "日报"}, block=True, priority=1)
total = on_command("总榜", aliases={"总排行", "排行", "排行榜"}, block=True, priority=1)
rate = on_command("进度", aliases={"战况", "现在情况", "当前进度"}, block=True, priority=1)

set_img = on_command("设置作业", block=True, priority=1)
get_img = on_command("获取作业", block=True, priority=1)


@set_img.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 获取消息中的图片url
    message = str(event.get_message())
    match = pattern.search(message)
    if not match:
        await set_img.finish("图呢？")
    url = match.group(1)

    # 下载并存储图片
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        file_path = Path(BASE_PATH) / "payload" / "cache" / "homework.jpg"
        with open(file_path, "wb") as f:
            f.write(response.content)
    # response = requests.get(url)
    # with open(Path(BASE_PATH) / "payload" / "cache" / "homework.jpg", "wb") as f:
    #     f.write(response.content)

    await set_img.send("设置成功")


@get_img.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    img_path = Path(BASE_PATH) / "payload" / "cache" / "homework.jpg"
    if not img_path.exists():
        await set_img.finish("没有找到图片文件，请先设置作业。")
    else:
        await set_img.send(MessageSegment.image("file:///" + str(img_path)))


# 日报
@daily.handle()
@is_level_A
async def send_daily_report(bot: Bot, event: GroupMessageEvent, cost=0):
    msg = str(event.get_message()).split()

    if len(msg) not in (1, 2):
        await daily.finish("请求格式错误，举例：\n战报\n战报 2023-03-20")

    try:
        if len(msg) == 1:
            img_path = await get_data()
        else:
            img_path = await get_data(msg[1])
    except Exception as e:
        await daily.finish(f"获取数据失败，错误信息：{e}")

    await daily.send(MessageSegment.image("file:///" + img_path))


@total.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    msg = str(event.get_message()).split()
    if len(msg) != 1:
        await daily.finish("请求格式错误，举例：\n总榜")

    try:
        img_path = await get_data_total()
    except Exception as e:
        await daily.finish(f"获取数据失败，错误信息：{e}")

    await daily.send(MessageSegment.image("file:///" + img_path))


@rate.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    msg = str(event.get_message()).split()
    if len(msg) != 1:
        await daily.finish("请求格式错误，举例：\n进度")

    try:
        img_path = await get_rate()
    except Exception as e:
        await daily.finish(f"获取数据失败，错误信息：{e}")

    await daily.send(MessageSegment.image("file:///" + img_path))
