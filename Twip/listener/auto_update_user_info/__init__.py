'''
Author: 七画一只妖
Date: 2022-01-22 21:42:01
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-10 10:40:02
Description: file content
'''
import re
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent


from .database import start


from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name='静默者-信息更新',
    description='功能：记录每个人的发言数量总数',
    usage='''使用方式：无【静默模块】''',
    extra={'version': 'v0.0.1',
           'cost': '###0'}
)


# 注册消息响应器
message_handle = on_message(block=False, priority=1)


@message_handle.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    # print(recall_user_info)
    try:
        user_name = recall_user_info['nickname']
    except:
        user_name = "不规范的值"
    # user_name = re.findall(r'[\u4e00-\u9fa5]', user_name) # 使用通配符只匹配汉字
    # user_name = "".join(user_name)
    start(user_name=user_name, user_id=user_id)