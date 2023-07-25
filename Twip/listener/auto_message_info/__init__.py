'''
Author: 七画一只妖
Date: 2022-01-23 13:17:33
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-25 09:23:41
Description: file content
'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from .db import insert_into_sql


from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name='静默者-消息记录',
    description='功能：记录机器人所在群每条发言记录',
    usage='''使用方式：无【静默模块】''',
    extra={'version': 'v0.0.1',
           'cost': '无消耗'}
)


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