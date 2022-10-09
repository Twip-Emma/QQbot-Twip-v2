'''
Author: 七画一只妖
Date: 2022-01-29 13:26:00
LastEditors: 七画一只妖
LastEditTime: 2022-08-30 11:26:52
Description: file content
'''
from typing import Union
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Bot
from tool.find_power.format_data import is_level_S

# 注册消息响应器
common_help = on_command('common_help', aliases={'测试'})


@common_help.handle()
@is_level_S
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot):
    await common_help.finish("用于判断机器人是否正常运行")
