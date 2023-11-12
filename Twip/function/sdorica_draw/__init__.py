'''
Author: 七画一只妖
Date: 2022-03-16 18:36:16
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-12 21:03:29
Description: file content
'''
import time
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_A
from tool.utils.logger import logger as my_logger

from .payload import get_drow, user_ill

__plugin_meta__ = PluginMetadata(
    name='万象抽卡',
    description='模拟万象物语抽卡',
    usage='''万象十连|万象图鉴''',
    extra={'version': 'v2.0.0',
           'cost': '30'}
)


sdorica_draw = on_command("万象十连", block=True, priority=2)
sdorica_ill = on_command("万象图鉴", block=True, priority=2)


@sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    t1 = time.time()
    user_id = str(event.user_id)
    re = await get_drow.drow(user_id)
    t2 = time.time()
    print_log(t2-t1, user_id, "万象十连")
    if not re:
        await sdorica_draw.send("今日抽卡已达上限5次")
    else:
        await sdorica_draw.send(MessageSegment.image(f"file:///{re}"))


@sdorica_ill.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=0):
    t1 = time.time()
    user_id = str(event.user_id)
    re = await user_ill.get_user_ill(user_id)
    t2 = time.time()
    print_log(t2-t1, user_id, "图鉴查看")
    await sdorica_ill.send(MessageSegment.image(f"file:///{re}"))


def print_log(t, user_id, draw_type) -> None:
    my_logger.success(
        '万象抽卡', f'<m>{"{:.3f}".format(t)}秒</m>成功发送：用户：<m>{user_id}</m> | 命令类型：<m>{draw_type}</m>')