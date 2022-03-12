'''
Author: 七画一只妖
Date: 2022-03-12 19:45:45
LastEditors: 七画一只妖
LastEditTime: 2022-03-12 21:02:02
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from .function import *


SUPER = "1157529280"


up_coin = on_command('增加原初能量')
down_coin = on_command('减少原初能量')



@up_coin.handle()
async def _(bot: Bot, event: MessageEvent):
    if str(event.user_id) != SUPER:
        await up_coin.finish()
    msg = str(event.get_message()).split()
    if len(msg) == 2:
        new = coin_up(int(msg[1]))
        await up_coin.finish(f"增加成功，你剩余的原初之力：{new}")
    else:
        await up_coin.finish("请输入正确的参数,用空格分开")


@down_coin.handle()
async def _(bot: Bot, event: MessageEvent):
    if str(event.user_id) != SUPER:
        await down_coin.finish()
    msg = str(event.get_message()).split()
    if len(msg) == 2:
        new = coin_down(int(msg[1]))
        await down_coin.finish(f"减少成功，你剩余的原初之力：{new}")
    else:
        await down_coin.finish("请输入正确的参数,用空格分开")