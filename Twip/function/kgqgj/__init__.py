'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:01:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-07 13:31:49
FilePath: \060坎公骑冠剑会战工具\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import re
from pathlib import Path

import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_A

from .payload.dao import get_data, get_data_total, get_rate
from .payload2.data_format import all_report, today_report

BASE_PATH: str = Path(__file__).absolute().parents[0]
pattern = re.compile(r"url=(.*?)&amp;")

__plugin_meta__ = PluginMetadata(
    name='坎公会战',
    description='提供《坎公骑冠剑》公会战的查询功能',
    usage='''日报/总榜/进度/千里眼/周边/设置作业/获取作业''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)

daily = on_command("日报", aliases={"x每日战报", "x每日", "x日报"}, block=True, priority=1)
total = on_command("总榜", aliases={"x总排行", "x排行", "x排行榜"}, block=True, priority=1)
rate = on_command("进度", aliases={"x战况", "x现在情况", "x当前进度"}, block=True, priority=1)
long_eyes = on_command("千里眼", block=True, priority=1)
toy = on_command("周边", block=True, priority=1)

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
    if len(msg) != 1:
        await daily.finish("请求格式错误，举例：\n日报")
        
    img_path = await today_report(event.get_user_id())
    # try:
    #     img_path = await today_report(event.get_user_id())
    # except Exception as e:
    #     await daily.finish(f"获取数据失败，错误信息：{e}")

    await daily.send(MessageSegment.image("file:///" + img_path))


@total.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    msg = str(event.get_message()).split()
    if len(msg) != 1:
        await daily.finish("请求格式错误，举例：\n总榜")

    try:
        img_path = await all_report(event.get_user_id())
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


@long_eyes.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await long_eyes.send(MessageSegment.image(f"https://cdngoapl.twip.top/%E5%9D%8E%E5%85%AC/longeyes20230601.png"))


@toy.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await toy.send(MessageSegment.image(f"http://cdngoapl.twip.top/%E5%9D%8E%E5%85%AC/%E5%91%A8%E8%BE%B920230531.png"))

