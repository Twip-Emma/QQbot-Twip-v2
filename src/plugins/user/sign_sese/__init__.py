'''
Author: 七画一只妖
Date: 2022-06-18 22:19:38
LastEditors: 七画一只妖
LastEditTime: 2022-06-18 23:04:13
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from tool.find_power.format_data import is_level_S
from .user_function import function_main, add_word


sese_sign = on_command("涩涩求签")
sese_add = on_command("添加涩涩词条")


@sese_sign.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        await sese_sign.finish()
    user_id = str(event.user_id)
    await sese_sign.finish(message = function_main(user_id), at_sender = True)


@sese_add.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        await sese_add.finish()
    message = str(event.message).split(" ")
    if len(message) != 2:
        await sese_add.finish(message = "请输入正确的格式，格式为：添加涩涩词条 [涩涩词条]", at_sender = True)
    try:
        add_word(message[1])
    except Exception as e:
        await sese_add.finish(message = f"添加失败，错误信息：{e}", at_sender = True)
    await sese_add.finish(message = "添加成功", at_sender = True)