'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-03-18 21:58:52
Description: file content
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from pathlib import Path


BASE_PATH: str = Path(__file__).absolute().parents[0]


test = on_command("testbean1", block=True, priority=1)


# AI画画
@test.handle()
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # img_path1 = f"{BASE_PATH}\\1.png"
    img_path2 = f"{BASE_PATH}\\2.png"
    # await test.send(MessageSegment.image("file:///" + img_path1))
    await test.send(MessageSegment.image("file:///" + img_path2))
