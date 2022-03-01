'''
Author: 七画一只妖
Date: 2022-03-01 20:27:45
LastEditors: 七画一只妖
LastEditTime: 2022-03-01 20:53:11
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from tool.find_power.format_data import is_level_A

from .db import *


show_rank = on_command("查看水群排行")


@show_rank.handle()
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_A(event):
        await show_rank.finish()
    re = data_to_image(find_speak_rank())
    await show_rank.send(MessageSegment.image(re))
    