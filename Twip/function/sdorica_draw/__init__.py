'''
Author: 七画一只妖
Date: 2022-03-16 18:36:16
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-25 09:09:16
Description: file content
'''
import time
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_A
from tool.utils.logger import logger as my_logger

from .function_user import start

__plugin_meta__ = PluginMetadata(
    name='万象抽卡',
    description='模拟万象物语抽卡',
    usage='''起源十连|首发十连|盛夏十连|限定十连|群友十连|爱十连''',
    extra={'version': 'v1.0.0',
           'cost': '30/50'}
)


qy_sdorica_draw = on_command("起源十连", block=True, priority=2)
ss_sdorica_draw = on_command("盛夏十连", block=True, priority=2)
sd_sdorica_draw = on_command("限定十连", block=True, priority=2)
sf_sdorica_draw = on_command("首发十连", block=True, priority=2)
hp_sdorica_draw = on_command("群友十连", block=True, priority=2)
ai_draw = on_command("爱十连", block=True, priority=2)


@qy_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    t1 = time.time()
    user_id = str(event.user_id)
    re = start(user_id,"起源十连")
    t2 = time.time()
    print_log(t2-t1, user_id, "起源十连")
    if re:
        # await qy_sdorica_draw.send(re)
        if "Error" in re:
            await qy_sdorica_draw.send(re)
        else:
            await qy_sdorica_draw.send(MessageSegment.image(re))
    else:
        await qy_sdorica_draw.send("出现了一点问题，请联系开发者七画")


@ss_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    user_id = str(event.user_id)
    re = start(user_id,"盛夏十连")
    if re:
        # await ss_sdorica_draw.send(re)
        if "Error" in re:
            await ss_sdorica_draw.send(re)
        else:
            await ss_sdorica_draw.send(MessageSegment.image(re))
    else:
        await ss_sdorica_draw.send("出现了一点问题，请联系开发者七画")


@sd_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    user_id = str(event.user_id)
    re = start(user_id,"限定十连")
    if re:
        # await sd_sdorica_draw.send(re)
        if "Error" in re:
            await sd_sdorica_draw.send(re)
        else:
            await sd_sdorica_draw.send(MessageSegment.image(re))
    else:
        await sd_sdorica_draw.send("出现了一点问题，请联系开发者七画")


@sf_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    user_id = str(event.user_id)
    re = start(user_id,"首发十连")
    if re:
        # await sf_sdorica_draw.send(re)
        if "Error" in re:
            await sf_sdorica_draw.send(re)
        else:
            await sf_sdorica_draw.send(MessageSegment.image(re))
    else:
        await sf_sdorica_draw.send("出现了一点问题，请联系开发者七画")


@hp_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=30):
    t1 = time.time()
    user_id = str(event.user_id)
    re = start(user_id,"群友十连")
    t2 = time.time()
    print_log(t2-t1, user_id, "群友十连")
    if re:
        # await sf_sdorica_draw.send(re)
        if "Error" in re:
            await hp_sdorica_draw.send(re)
        else:
            await hp_sdorica_draw.send(MessageSegment.image(re))
    else:
        await hp_sdorica_draw.send("出现了一点问题，请联系开发者七画")


@ai_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent, cost=50):
    t1 = time.time()
    user_id = str(event.user_id)
    re = start(user_id,"爱十连")
    t2 = time.time()
    print_log(t2-t1, user_id, "爱十连")
    if re:
        # await sf_sdorica_draw.send(re)
        if "Error" in re:
            await ai_draw.send(re)
        else:
            await ai_draw.send(MessageSegment.image(re))
    else:
        await ai_draw.send("出现了一点问题，请联系开发者七画")


def print_log(t, user_id, draw_type) -> None:
    my_logger.success(
        '万象抽卡', f'<m>{"{:.3f}".format(t)}秒</m>成功发送：用户：<m>{user_id}</m> | 抽卡类型：<m>{draw_type}</m>')