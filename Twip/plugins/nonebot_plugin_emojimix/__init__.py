'''
Author: 七画一只妖
Date: 2022-04-16 16:50:54
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-13 19:09:21
Description: file content
'''
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.params import RegexDict
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import delete_user_coin

from .data_source import mix_emoji

__plugin_meta__ = PluginMetadata(
    name='表情混合',
    description='发送两个表情进行混合',
    usage='''使用方式<emoji> + <emoji>（示例）😎+😁''',
    extra={'version': 'v1.0.0',
           'cost': '###9'}
)


pattern = "[\u200d-\U0001fab5]"
emojimix = on_regex(
    rf"^(?P<code1>{pattern})\s*\+\s*(?P<code2>{pattern})$", block=True, priority=1
)


__help__plugin_name__ = "emojimix"
__des__ = "emoji合成器"
__cmd__ = "{emoji1}+{emoji2}"
__short_cmd__ = __cmd__
__example__ = "😎+😁"
__usage__ = f"{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}"


@emojimix.handle()
async def _(event:GroupMessageEvent,msg: dict = RegexDict()):

    if not delete_user_coin(str(event.user_id), 9):
        return 

    emoji_code1 = msg["code1"]
    emoji_code2 = msg["code2"]
    result = await mix_emoji(emoji_code1, emoji_code2)
    if isinstance(result, str):
        await emojimix.finish(result)
    else:
        await emojimix.finish(MessageSegment.image(result))
