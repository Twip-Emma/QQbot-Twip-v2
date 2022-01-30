'''
Author: 七画一只妖
Date: 2022-01-19 21:32:13
LastEditors: 七画一只妖
LastEditTime: 2022-01-31 05:01:20
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from tool.find_power.format_data import is_level_S

from .data_source import get_weather_of_city

weather = on_command("天气", rule=to_me(), priority=5)


CITY = ""


@weather.handle()
async def handle_first_receive(event: MessageEvent):
    if not is_level_S(event):
        await weather.finish()
    global CITY
    args = str(event.get_message()).split()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    try:
        # city_weather = await get_weather(args[1])
        city_weather = await get_weather_of_city(city=args[1])
        await weather.send(message=city_weather)
    except:
        await weather.send("请输入你要查询的天气\n比如发送：天气 北京")



async def get_weather(city: str):
    message = get_weather_of_city(city=city)
    return message
