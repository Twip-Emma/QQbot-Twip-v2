'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-02-14 13:57:00
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-05-10 10:39:17
'''
from nonebot import on_command
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent
from nonebot.params import CommandArg, ArgStr
from .data import text_to_emoji
from tool.find_power.format_data import is_level_S

abstract = on_command("abstract", aliases={
                      "抽象", "抽象化"}, priority=5, block=True)


@abstract.handle()
@is_level_S
async def _(state: T_State, event: GroupMessageEvent, cost=10, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["abstract"] = arg.extract_plain_text().strip()


@abstract.got("abstract", prompt="你要抽象什么？")
async def _(bot: Bot, event: Event, target_text: str = ArgStr("abstract")):
    abstract_responses = text_to_emoji(target_text)
    if abstract_responses:
        logger.info("抽象成功！")
        await abstract.send(abstract_responses)
    else:
        logger.error("抽象失败~")
        await abstract.send("抽象异常了~一定是程序出了点问题！")
