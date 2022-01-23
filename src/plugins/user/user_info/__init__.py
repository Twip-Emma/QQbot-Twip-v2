'''
Author: 七画一只妖
Date: 2022-01-23 10:46:54
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 13:46:03
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from .function import start


get_info = on_command("个人信息")


@get_info.handle()
async def _(bot: Bot,event:GroupMessageEvent):
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    # await get_luck.finish("hi")
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']
    imgb64 = start(user_name=recall_user_name,user_id=user_id)
    await get_info.finish(MessageSegment.image(imgb64))