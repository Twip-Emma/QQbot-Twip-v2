'''
Author: 七画一只妖
Date: 2022-03-16 18:36:16
LastEditors: 七画一只妖
LastEditTime: 2022-08-28 22:43:44
Description: file content
'''
from .function_user import start

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

from tool.find_power.format_data import is_level_S


qy_sdorica_draw = on_command("起源十连", block=True, priority=2)
ss_sdorica_draw = on_command("盛夏十连", block=True, priority=2)
sd_sdorica_draw = on_command("限定十连", block=True, priority=2)
sf_sdorica_draw = on_command("首发十连", block=True, priority=2)
hp_sdorica_draw = on_command("群友十连", block=True, priority=2)


@qy_sdorica_draw.handle()
@is_level_S
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await qy_sdorica_draw.finish()
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
@is_level_S
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await ss_sdorica_draw.finish()
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
@is_level_S
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await sd_sdorica_draw.finish()
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
@is_level_S
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await sf_sdorica_draw.finish()
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
@is_level_S
async def _(bot:Bot,event: GroupMessageEvent):
    if not is_level_S(event):
        await hp_sdorica_draw.finish()
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