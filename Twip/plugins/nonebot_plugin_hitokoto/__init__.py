'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-07-25 17:27:05
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-05 21:58:26
'''
import httpx
from nonebot import logger, on_command
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

hitokoto_matcher = on_command("一言", aliases={"一句"})

__plugin_meta__ = PluginMetadata(
    name='一言',
    description='提供群文件直链的获取',
    usage='''一言/一句''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)

@hitokoto_matcher.handle()
async def hitokoto(matcher: Matcher, args: Message = CommandArg()):
    if args:
        return
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=h")
    if response.is_error:
        logger.error("获取一言失败")
        return
    data = response.json()
    msg = data["hitokoto"]
    add = ""
    if works := data["from"]:
        add += f"《{works}》"
    if from_who := data["from_who"]:
        add += f"{from_who}"
    if add:
        msg += f"\n——{add}"
    await matcher.finish(msg)
