'''
Author: 七画一只妖
Date: 2022-03-11 17:10:02
LastEditors: 七画一只妖
LastEditTime: 2022-03-13 10:12:29
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .get_image import *


SUPER = "1157529280"


message_recall = on_command('恢复数据')


@message_recall.handle()
async def _(bot: Bot, event: MessageEvent):
    if str(event.user_id) != SUPER:
        await message_recall.finish()
    msg = str(event.get_message()).split()
    if len(msg) == 3:
        im_data = start(group_id=msg[1],count=msg[2])
        await message_recall.finish(MessageSegment.image(im_data))
    else:
        await message_recall.finish("请输入正确的参数,用空格分开")