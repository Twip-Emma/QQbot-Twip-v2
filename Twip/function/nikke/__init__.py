'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-08-10 09:18:08
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-10 09:38:00
'''
import asyncio
import random
import re
from pathlib import Path

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_A
from tool.QsPilUtils2.dao import text_to_image


BASE_PATH: str = Path(__file__).absolute().parents[0]
pattern = re.compile(r"url=(.*?)&amp;")

__plugin_meta__ = PluginMetadata(
    name='NIKKE攻略',
    description='提供《NIKKE》各种攻略表的查询',
    usage='''NIKKE帮助/妮姬帮助/NIKKE强度/妮姬强度''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)


help = on_command("NIKKE帮助", aliases={
                  "妮姬帮助", "nikke帮助"}, block=True, priority=1)
rank = on_command("NIKKE强度", aliases={
                  "妮姬强度", "妮姬强度表", "nikke强度", "nikke强度表", "妮姬节奏", "妮姬节奏表", "妮姬节奏榜"}, block=True, priority=1)


@help.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    message = """
    NIKKE-帮助
    可支持的指令有：
        NIKKE强度/妮姬强度  查看强度表
    """
    await help.send(MessageSegment.image(f"file:///{text_to_image(message,15,(20,20))}"))


@rank.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    message = f"正在发送，图片较多（共3张）请稍等..."
    await rank.send(MessageSegment.image(f"file:///{text_to_image(message,15,(20,20))}"))
    await asyncio.sleep(random.randint(1, 3))
    await rank.send(MessageSegment.image(f"https://cdngoapl.twip.top/NIKKE/%E5%A6%AE%E5%A7%AC%E5%BC%BA%E5%BA%A6%E8%A1%A8A-1.jpg"))
    await asyncio.sleep(random.randint(1, 3))
    await rank.send(MessageSegment.image(f"https://cdngoapl.twip.top/NIKKE/%E5%A6%AE%E5%A7%AC%E5%BC%BA%E5%BA%A6%E8%A1%A8B-1.jpg"))
    await asyncio.sleep(random.randint(1, 3))
    await rank.send(MessageSegment.image(f"https://cdngoapl.twip.top/NIKKE/%E5%A6%AE%E5%A7%AC%E5%BC%BA%E5%BA%A6%E8%A1%A8C-1.jpg"))