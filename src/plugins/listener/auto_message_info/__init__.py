'''
Author: 七画一只妖
Date: 2022-01-23 13:17:33
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 13:19:14
Description: file content
'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from os import path
from .db import *


# 注册消息响应器
message_handle = on_message()


@message_handle.handle()
async def _(event: GroupMessageEvent):
    message = event.msg
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    message_id = str(event.message_id)
    insert_into_sql(message_id,message,group_id,user_id)