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
    url = host + urllib.parse.quote(city)
    r = requests.get(url)
    jsons = json.loads(r.text)
    str = city+'的天气：\n'
    len = 0
    for i in jsons['data']['forecast']:
        if len < 2:
            if len == 0:
                str += '今日：'
            if len == 1:
                str += '明日：'
            str += i['date']
            str += '\n天气：'
            str += i['type']
            str += '\n最'
            str += i['low']
            str += '\n最'
            str += i['high']
            str += '\n'
            len += 1
    return str