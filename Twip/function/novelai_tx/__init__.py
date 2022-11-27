'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-11-27 22:38:30
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-11-27 23:56:11
'''
import json
from base64 import b64encode
from io import BytesIO
from json import dumps
from pathlib import Path

import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, Message,
                                         MessageSegment)
from nonebot.params import Arg, CommandArg, State
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from PIL import Image

from tool.find_power.format_data import is_level_S
from tool.utils.logger import logger as my_logger

BASE_PATH: str = Path(__file__).absolute().parents[0]


aihuahua = on_command("ai画画", aliases={"ai_painting"}, block=True, priority=1)


@aihuahua.handle()
@is_level_S
async def handle_first_receive(event: GroupMessageEvent, cost=20, state: T_State = State(), img: Message = CommandArg()):
    if img:
        state["img"] = img


@aihuahua.got("img", prompt="发一张你要生成的图")
async def get_setu(bot: Bot,
                   event: GroupMessageEvent,
                   msg: Message = Arg("img")):
    try:
        if msg[0].type == "image":
            await bot.send(event=event, message="正在处理图片，可能要等比较久的时间！")
            url = msg[0].data["url"]  # 图片链接

            # 图片url转bytes
            res = requests.get(url)
            byte_stream = BytesIO(res.content)
            roiImg = Image.open(byte_stream)
            imgByteArr = BytesIO()
            roiImg.save(imgByteArr, format="PNG")
            imgByteArr = imgByteArr.getvalue()

            payload = {
                "busiId": "ai_painting_anime_entry",
                "images": [b64encode(imgByteArr).decode()],
                "extra": dumps({
                    "platfrom": "web",
                    "data_report": {
                        "parent_trace_id": "7c0a9e89-bcf7-3142-8df2-d0c0ae894404",
                        "root_channel": "qq_sousuo",
                        "level": 1,
                    },
                }),
            }

            r = requests.post(
                "https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process", json=payload)

            re_data: dict = r.json()
            if re_data["code"] == 0:
                a = re_data["extra"]
                b = json.loads(a)
                img_url = b["img_urls"][2]

                res2 = requests.get(img_url)
                byte_stream2 = BytesIO(res2.content)
                roiImg = Image.open(byte_stream2)

                box = (30, 30, 795, 1180)
                roiImg = roiImg.crop(box)

                roiImg.save(f"{BASE_PATH}\\images\\{event.get_user_id()}.jpg")
                await bot.send(event=event, message=MessageSegment.image(f"file:///{BASE_PATH}\\images\\{event.get_user_id()}.jpg"))
            else:
                await bot.send(event=event, message=f"失败！\n状态码：{re_data['code']}\n返回信息：{re_data['msg']}")

    except Exception as e:
        await bot.send(event=event, message=f"发送错误！\n类型为：{type(e)}")
