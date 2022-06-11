'''
Author: 七画一只妖
Date: 2022-06-06 18:37:17
LastEditors: 七画一只妖
LastEditTime: 2022-06-10 15:41:43
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from tool.find_power.format_data import is_level_S
from .get_user_data import get_data_and_format


get_info_new = on_command("个人信息")


@get_info_new.handle()
async def _(event: GroupMessageEvent):
    if not is_level_S(event):
        return
    await get_info_new.send(at_sender = True, message=get_data_and_format(str(event.user_id)))
