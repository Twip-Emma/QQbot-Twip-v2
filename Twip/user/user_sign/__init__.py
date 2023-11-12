'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-12 13:32:01
Description: file content
'''

import time

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_S
from tool.utils.logger import logger as my_logger

from .payload import user_pkg

__plugin_meta__ = PluginMetadata(
    name='求签系统',
    description='获得一张引子',
    usage='''使用方式：求签''',
    extra={'version': 'v2.0.0',
           'cost': '15'}
)


get_luck = on_command("求签", block=True, priority=2)


# 求签
@get_luck.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost=15):
    t1 = time.time()
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    # await get_luck.finish("hi")
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    message_image = await user_pkg.get_sign(user_id, recall_user_name)
    t2 = time.time()
    await get_luck.send(MessageSegment.image("file:///" + message_image))
    my_logger.success(
        '求签系统', f'<m>{"{:.3f}".format(t2-t1)}秒</m>成功发送：用户：<m>{recall_user_name}{user_id}</m> | 群：<m>{group_id}</m>')