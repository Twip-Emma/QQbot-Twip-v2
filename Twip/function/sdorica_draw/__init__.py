'''
Author: 七画一只妖
Date: 2022-03-16 18:36:16
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 15:24:47
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_A

from .function_user import start

__plugin_meta__ = PluginMetadata(
    name='原神抽卡',
    description='模拟万象物语抽卡',
    usage='''起源十连|首发十连|盛夏十连|限定十连|群友十连''',
    extra={'version': 'v1.0.0',
           'cost': '#150'}
)


qy_sdorica_draw = on_command("起源十连", block=True, priority=2)
ss_sdorica_draw = on_command("盛夏十连", block=True, priority=2)
sd_sdorica_draw = on_command("限定十连", block=True, priority=2)
sf_sdorica_draw = on_command("首发十连", block=True, priority=2)
hp_sdorica_draw = on_command("群友十连", block=True, priority=2)


@qy_sdorica_draw.handle()
@is_level_A
async def _(bot:Bot,event: GroupMessageEvent):
    user_id = str(event.user_id)
    re = start(user_id,"起源十连")
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
async def _(bot:Bot,event: GroupMessageEvent):
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
async def _(bot:Bot,event: GroupMessageEvent):
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
async def _(bot:Bot,event: GroupMessageEvent):
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
async def _(bot:Bot,event: GroupMessageEvent):
    user_id = str(event.user_id)
    re = start(user_id,"群友十连")
    if re:
        # await sf_sdorica_draw.send(re)
        if "Error" in re:
            await hp_sdorica_draw.send(re)
        else:
            await hp_sdorica_draw.send(MessageSegment.image(re))
    else:
        await hp_sdorica_draw.send("出现了一点问题，请联系开发者七画")
