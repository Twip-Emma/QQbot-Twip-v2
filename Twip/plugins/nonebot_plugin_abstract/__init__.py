'''
Author: 七画一只妖
Date: 2022-04-22 21:22:27
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-13 19:02:05
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, Message
from nonebot.log import logger
from nonebot.params import ArgStr, CommandArg, State
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from tool.find_power.format_data import is_level_S

from .data import text_to_emoji

__plugin_meta__ = PluginMetadata(
    name='语句抽象',
    description='抽象你说的一段话',
    usage='''抽象|抽象化 <你想说的话>''',
    extra={'version': 'v1.0.0',
           'cost': '###7'}
)


abstract = on_command("abstract", aliases={"抽象", "抽象化"})

@abstract.handle()
@is_level_S
async def _(event:GroupMessageEvent,state: T_State = State(), arg: Message = CommandArg(),cost=7):

    if not is_level_S(event):
        await abstract.finish()

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
