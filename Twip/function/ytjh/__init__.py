'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:01:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-24 09:52:50
FilePath: \060坎公骑冠剑会战工具\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
from pathlib import Path


from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from tool.find_power.format_data import is_level_A

BASE_PATH: str = Path(__file__).absolute().parents[0]
pattern = re.compile(r"url=(.*?)&amp;")


suanfa = on_command("云图算法", aliases={"云图算法表", "云图算法榜"}, block=True, priority=1)
rank = on_command("云图强度", aliases={"云图强度表", "云图强度榜", "云图节奏", "云图节奏表", "云图节奏榜"}, block=True, priority=1)
yinji = on_command("云图印记", aliases={"云图印记表", "云图印记榜"}, block=True, priority=1)
yuntu_help = on_command("云图帮助", aliases={"云图帮助表", "帮助云图", "云图 帮助"}, block=True, priority=1)


@suanfa.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await suanfa.send(message="正在发送，图片较大（19MB）请稍等...")
    await suanfa.send(MessageSegment.image(f"https://cdngoapl.twip.top/%E4%BA%91%E5%9B%BE/%E7%AE%97%E6%B3%95%E8%A1%A8-%E5%8E%8B%E7%BC%A9.png"))


@rank.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await rank.send(MessageSegment.image(f"https://cdngoapl.twip.top/%E4%BA%91%E5%9B%BE/%E5%BC%BA%E5%BA%A6%E8%A1%A82.png"))


@yinji.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await yinji.send(MessageSegment.image(f"https://cdngoapl.twip.top/%E4%BA%91%E5%9B%BE/%E5%8D%B0%E8%AE%B0%E8%A1%A82.jpg"))


@yuntu_help.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    await yuntu_help.send(message="""
    云图计划-帮助
    可支持的指令有：
        云图算法
        云图强度
        云图印记
    """)

