'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖
LastEditTime: 2022-01-18 21:49:12
Description: file content
'''

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.rule import to_me

# from tool.black_list_ad.group_black import get_power_in_sdorica
from .sign import check_user_sign
from .sign_daily import sign_daily_start


get_luck = on_command("求签", rule=to_me())
user_sign = on_command("签到", rule=to_me())


# 求签
# @get_power_in_sdorica
@get_luck.handle()
async def _(bot: Bot, event: Event, state: T_State):
    user_id = str(event.get_user_id)
    # group_id = str(event.get_group_id)
    # group_id = str(event.get_session_id)
    # print(group_id)
    await get_luck.finish("hi")
    # recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    # recall_user_name = recall_user_info['nickname']

    # message = check_user_sign(user_id, recall_user_name)
    # await session.send(message)


# 签到（新版）
@user_sign.handle()
# @get_power_in_sdorica
async def _(bot: Bot, event: Event):
    # user_id = str(event.get_user_id)
    # group_id = str(session.event.group_id)
    # recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    # user_name = recall_user_info['nickname']
    # msg = sign_daily_start(user_name=user_name, user_id=user_id)
    # await session.send(message=msg)
    pass
