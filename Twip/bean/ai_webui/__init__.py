'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-01-30 11:22:17
Description: file content
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.utils.logger import logger as my_logger

from .user_function import get_image


ai_p = on_command("AI画画", block=True, priority=2)


# 求签
@ai_p.handle()
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    if user_id != "1157529280":
        return

    msg = str(event.get_message()).split()
    if len(msg) == 1:
        await ai_p.finish("请在后面空格接上词条")
    else:
        await ai_p.send("开始绘画，请等待大约20秒~")

        msg = str(event.get_message()).split("AI画画 ")
        ap = msg[1]
        await ai_p.send(MessageSegment.image("file:///" + await get_image(ap, user_id)))

    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    my_logger.success(
        'AI画画WEBUI', f'成功发送：用户：<m>{recall_user_name}{user_id}</m> | 群：<m>{group_id}</m>')