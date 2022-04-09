'''
Author: 七画一只妖
Date: 2022-01-23 10:46:54
LastEditors: 七画一只妖
LastEditTime: 2022-04-09 14:17:18
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from tool.find_power.format_data import is_level_S
from .function import start


get_info = on_command("个人信息")


@get_info.handle()
async def _(bot: Bot,event:GroupMessageEvent):
    if not is_level_S(event):
            return
    try:
        user_id = str(event.user_id)
        imgb64 = start(user_id=user_id)
        await get_info.send(MessageSegment.image("file:///" + imgb64))
    except Exception as e:
        await get_info.send(f"type:{type(e)}")