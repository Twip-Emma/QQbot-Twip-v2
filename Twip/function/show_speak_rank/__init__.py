'''
Author: 七画一只妖
Date: 2022-03-01 20:27:45
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 15:22:02
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from tool.find_power.format_data import is_level_A

from .db import *

__plugin_meta__ = PluginMetadata(
    name='水群排行',
    description='查看机器人所有群综合的水群排行榜前99名',
    usage='''查看水群排行''',
    extra={'version': 'v1.0.0',
           'cost': '#300'}
)


SUPER = "1157529280"

show_rank = on_command("查看水群排行", block=True, priority=2, state={
    'pm_usage': '查看水群排行',
    'pm_describe': '查看所有群的水群前99名',
    'pm_priority': 2
})
show_rank_admin = on_command("查看水群排行-开发者模式", block=True, priority=2, state={
    'pm_usage': '**查看水群排行-开发者模式',
    'pm_describe': '查看所有群的水群前99名，显示完整QQ号',
    'pm_priority': 2
})


@show_rank.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent):
    re = data_to_image(find_speak_rank(),"user")
    await show_rank.send(MessageSegment.image(re))


@show_rank_admin.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent):
    if str(event.user_id) != SUPER:
        return
    re = data_to_image(find_speak_rank(),"admin")
    await show_rank.send(MessageSegment.image(re))
    