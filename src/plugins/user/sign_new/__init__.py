'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖
LastEditTime: 2022-09-17 13:20:17
Description: file content
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_S

from .sign import user_sign_main

__plugin_meta__ = PluginMetadata(
    name='求签',
    description='向境神求签，获得一张引子',
    usage='求签',
    extra={
        'priority': 2,
    }
)


get_luck = on_command("求签", block=True, priority=2, state={
        'pm_name':        '求签',
        'pm_description': '向境神求签，获得一张引子',
        'pm_usage':       '求签',
        'pm_priority':    2
    })
# user_sign = on_command("-签到")



# @get_luck.handle()
# @on_command('weather', aliases=('的天气', '天气预报', '查天气'),only_to_me=False)


# 求签
@get_luck.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    # await get_luck.finish("hi")
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    message_image = user_sign_main(user_id, recall_user_name)
    await get_luck.send(MessageSegment.image(message_image))


# 签到（新版）
# @user_sign.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
#     if not is_level_S(event):
#         await get_luck.finish()
#     group_id = str(event.group_id)
#     user_id = str(event.user_id)
#     recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
#     user_name = recall_user_info['nickname']
#     message = sign_daily_start(user_name=user_name, user_id=user_id)
#     # await session.send(message=msg)
#     await get_luck.finish(message)


# def img_to_b64(pic: Image.Image) -> str:
#     buf = BytesIO()
#     pic.save(buf, format="PNG")
#     base64_str = base64.b64encode(buf.getbuffer()).decode()
#     return "base64://" + base64_str
