'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-02-14 15:18:53
Description: file content
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_A
from tool.utils.logger import logger as my_logger

from tool.find_power.user_database import get_user_info_new, insert_user_info_new


__plugin_meta__ = PluginMetadata(
    name='个人信息',
    description='查看自己的行动点和健康值',
    usage='''使用方式：个人信息''',
    extra={'version': 'v1.0.0',
           'cost': '###0'}
)


get_luck = on_command("个人信息", block=True, priority=2)


# 求签
@get_luck.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    group_id = str(event.group_id)
    user_id = str(event.user_id)

    user_data = get_user_info_new(user_id=user_id)
    if user_data == None:
        insert_user_info_new(user_id=user_id)
        user_data = get_user_info_new(user_id=user_id)
    
    await get_luck.send(message=f"你的个人信息如下：\n行动点：{user_data[1]}/{user_data[4]}\n健康值：{user_data[2]}/100\n画境币：{user_data[3]}", at_sender=True)
    
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    my_logger.success(
        '个人信息查询', f'成功发送：用户：<m>{recall_user_name}{user_id}</m> | 群：<m>{group_id}</m>')
