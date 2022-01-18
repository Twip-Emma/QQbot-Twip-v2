'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖
LastEditTime: 2022-01-18 22:05:25
Description: file content
'''

from nonebot import on_command
# from nonebot.adapters import Bot, Event, GroupMessageEvent
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me

# from tool.black_list_ad.group_black import get_power_in_sdorica
from .sign import check_user_sign
from .sign_daily import sign_daily_start


get_luck = on_command("求签", rule=to_me())
user_sign = on_command("签到", rule=to_me())


# 求签
@get_luck.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    # await get_luck.finish("hi")
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    message = check_user_sign(user_id, recall_user_name)
    # await session.send(message)
    await get_luck.finish(message)


# 签到（新版）
@user_sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    user_name = recall_user_info['nickname']
    message = sign_daily_start(user_name=user_name, user_id=user_id)
    # await session.send(message=msg)
    await get_luck.finish(message)
