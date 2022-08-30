'''
Author: 七画一只妖
Date: 2022-01-23 13:17:33
LastEditors: 七画一只妖
LastEditTime: 2022-08-30 11:02:00
Description: file content
'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from .db import insert_into_sql


# 注册消息响应器
message_handle = on_message(block=False, priority=1)


# 记录每条发言
@message_handle.handle()
async def _(event: MessageEvent, e: GroupMessageEvent):
    try:
        message = str(event.get_message())
    except:
        message = "消息错误，可能是太长了，这是个xml卡片或者分享链接"
    user_id = str(e.user_id)
    group_id = str(e.group_id)
    message_id = str(event.message_id)
    insert_into_sql(message_id, message, group_id, user_id)