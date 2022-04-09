'''
Author: 七画一只妖
Date: 2022-03-01 20:27:45
LastEditors: 七画一只妖
LastEditTime: 2022-04-07 09:15:38
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from tool.find_power.format_data import is_level_A,is_level_S

from .db import *


SUPER = "1157529280"

show_rank = on_command("查看水群排行")
show_rank_admin = on_command("查看水群排行-开发者模式")


@show_rank.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_A(event):
        return
    re = data_to_image(find_speak_rank(),"user")
    await show_rank.send(MessageSegment.image(re))


@show_rank_admin.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        return

    if str(event.user_id) != SUPER:
        return

    re = data_to_image(find_speak_rank(),"admin")
    await show_rank.send(MessageSegment.image(re))
    