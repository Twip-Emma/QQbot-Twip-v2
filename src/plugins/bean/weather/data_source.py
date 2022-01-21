'''
Author: 七画一只妖
Date: 2022-01-19 21:32:13
LastEditors: 七画一只妖
LastEditTime: 2022-01-21 12:21:54
Description: file content
'''
from urllib.request import urlopen
import urllib.request
import requests
import sys
import ssl
import importlib
importlib.reload(sys)
import json


async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    host = 'http://wthrcdn.etouch.cn/weather_mini?city='
    url = host + city
    r = requests.get(url)
    jsons = json.loads(r.text)
    re_msg = city+'的天气：\n'
    len = 0
    for i in jsons['data']['forecast']:
        if len < 2:
            if len == 0:
                re_msg += '今日：'
            if len == 1:
                re_msg += '明日：'
            re_msg += i['date']
            re_msg += '\n天气：'
            re_msg += i['type']
            re_msg += '\n最'
            re_msg += i['low']
            re_msg += '\n最'
            re_msg += i['high']
            re_msg += '\n'
            len += 1
    return re_msg