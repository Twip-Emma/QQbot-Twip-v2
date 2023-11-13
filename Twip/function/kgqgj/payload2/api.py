'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-06 23:32:24
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-13 15:04:51
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import hashlib
import time
import httpx
import binascii
import hashlib
import os
import time
from urllib.parse import urlencode
import json

from Twip import KGQGJ_COOKIE

# 全局变量下标
req_index = 0

with open("./config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

DATE_URL = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report_date"
DAILY_URL = "https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report"
RATE_URL = f"""https://api.game.bilibili.com/game/player/tools/kan_gong/fight_news"""

header = {
    "accept": f"text/htfml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": f"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "connection": f"keep-alive"}

header["cookie"] = KGQGJ_COOKIE


app_key = 'a5e793dd8b8e425c9bff92ed79e4458f'
app_secret = 'xoNO7qa9761mNPyLtTn8zxPeX80iLnDonYCOzqS7bG8='


# 获取日期
async def get_date():
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.get(url=DATE_URL, headers=header, params=get_sign())
        re_data: dict = r.json()
        await check_data(re_data)
        return re_data
    

async def get_daily():
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.get(url=DAILY_URL, headers=header, params=get_sign())
        re_data: dict = r.json()
        await check_data(re_data)
        return re_data
    

async def get_daily_target(date: str):
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.get(url=DAILY_URL, headers=header, params=get_sign(date))
        re_data: dict = r.json()
        await check_data(re_data)
        return re_data


async def get_rate_data():
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.get(url=RATE_URL, headers=header, params=get_sign())
        re_data: dict = r.json()
        await check_data(re_data)
        return re_data


# 获取sign
def get_sign(date: str = None) -> dict:
    data = {
        'ts': int(time.time()),
        'nonce': '-'.join([binascii.hexlify(os.urandom(3)).decode() for _ in range(3)]),
        'appkey': app_key
    }

    # 将sign加入到data里面
    if date:
        data['date'] = date

    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    sorted_params_str = urlencode(sorted_data)
    sign = hashlib.md5(
        (sorted_params_str + f'&secret={app_secret}').encode()).hexdigest()
    
    data['sign'] = sign

    return data


# 数据校验
async def check_data(data: dict) -> None:
    msg = f"接口错误码code: {data['code']}\n接口提示信息message: {data['message']}\n可能的解决办法:"
    if data["code"] == -101:
        msg += " 请检查cookies是否放好，如果放好了还是这个错误就去百宝袋更新cookies"
        raise RuntimeError(f"\n{msg}")
    elif data["code"] == -400:
        msg += " 请求接口的参数不对，请联系开发者修BUG"
        raise RuntimeError(f"\n{msg}")
    elif data["code"] == 11002:
        msg += " 这是校验失败，请联系开发者修BUG"
        raise RuntimeError(f"\n{msg}")
