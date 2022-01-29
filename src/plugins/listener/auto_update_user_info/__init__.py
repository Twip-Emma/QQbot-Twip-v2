'''
Author: 七画一只妖
Date: 2022-01-22 21:42:01
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 13:20:19
Description: file content
'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent


from .database import start


# 注册消息响应器
message_handle = on_message()


@message_handle.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    user_name = recall_user_info['nickname']
    start(user_name=user_name, user_id=user_id)