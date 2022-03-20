'''
Author: 七画一只妖
Date: 2022-01-23 10:46:54
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 13:59:21
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
        await get_info.finish()
    user_id = str(event.user_id)
    
    imgb64 = start(user_id=user_id)
    await get_info.finish(MessageSegment.image("file:///" + imgb64))