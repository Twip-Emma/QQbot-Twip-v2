'''
Author: 七画一只妖
Date: 2022-01-19 21:32:13
LastEditors: 七画一只妖
LastEditTime: 2022-01-19 21:40:10
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

weather = on_command("天气", rule=to_me(), priority=5)


CITY = ""


@weather.handle()
async def handle_first_receive(event: Event):
    global CITY
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        CITY = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city():
    global CITY
    city = CITY
    if city not in ["上海", "北京"]:
        await weather.reject("你想查询的城市暂不支持，请重新输入！")
    city_weather = await get_weather(city)
    await weather.finish(city_weather)


async def get_weather(city: str):
    return f"{city}的天气是..."