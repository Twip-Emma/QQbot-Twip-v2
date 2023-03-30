'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:01:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-03-27 16:01:51
FilePath: \060坎公骑冠剑会战工具\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pathlib import Path

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from .payload.dao import get_data, get_data_total

from tool.find_power.format_data import is_level_A

BASE_PATH: str = Path(__file__).absolute().parents[0]


daily = on_command("战报", aliases={"每日战报", "每日", "日报"}, block=True, priority=1)
total = on_command("总榜", aliases={"总排行", "排行", "排行榜"}, block=True, priority=1)


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