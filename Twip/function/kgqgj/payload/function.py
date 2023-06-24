'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:05:56
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-06-24 13:10:01
FilePath: \060坎公骑冠剑会战工具\function.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
from pathlib import Path
import requests
import httpx

from .setting import DAMAGE_URL, RATE_URL, DAO_IMAGE, DAO_DAILY, DAMAGE_TOTAL
from .cookies import header, header2, APP_KEY
from .utils.data_utils import save_data

BASE_PATH: str = Path(__file__).absolute().parents[0]


async def f_get_user_data(date:str) -> dict:

    url = f"""
https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?ts=1687582295973&nonce=f1e7b034-d50e-40fe-af1f-00af9fc212f2&appkey={APP_KEY}&sign=e3bca73d6c554cdb51a9ed05e5431497"""

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=url + date, headers=header)
            re_data: dict = r.json()
            save_data(f"{BASE_PATH}\\data\\user_data.json", re_data)
            data = re_data["data"]
            return data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}


async def f_get_damage_data(date:str):
    url = f"""https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?ts=1687582295973&nonce=f1e7b034-d50e-40fe-af1f-00af9fc212f2&appkey={APP_KEY}&sign=e3bca73d6c554cdb51a9ed05e5431497"""

    url2 = f"""https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?date={date}&ts=1687582528332&nonce=c05a9707-f5ee-42fc-87b5-3e4db005fb70&appkey={APP_KEY}&sign=7664f1d3cdb1316bcf123e3894efeee2"""
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            if date:
                r = await client.get(url=url2, headers=header)
            else:
                r = await client.get(url=url, headers=header)
            re_data: dict = r.json()
            save_data(f"{BASE_PATH}\\data\\damage_data.json", re_data)
            data = re_data["data"]
            return data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}


async def f_get_rate_data():
    url = f"""https://api.game.bilibili.com/game/player/tools/kan_gong/fight_news?ts=1687583171294&nonce=286263db-9437-493f-bc4f-25ec6b1326ee&appkey={APP_KEY}&sign=73bb681870500d80828ec38ebf751bbc"""
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=url, headers=header)
            re_data: dict = r.json()
            data = re_data["data"]
            return data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def f_get_dao_total():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAO_IMAGE, headers=header2)
            with open(f"{BASE_PATH}\\cache\\dao_total.jpg", "wb") as f:
                f.write(r.content)
        return f"{BASE_PATH}\\cache\\dao_total.jpg"
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def f_get_dao_daily():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAO_DAILY, headers=header2)
            with open(f"{BASE_PATH}\\cache\\dao_daily.jpg", "wb") as f:
                f.write(r.content)
        return f"{BASE_PATH}\\cache\\dao_daily.jpg"
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def f_get_damage_total():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAMAGE_TOTAL, headers=header2)
            with open(f"{BASE_PATH}\\cache\\damage_total.jpg", "wb") as f:
                f.write(r.content)
        return f"{BASE_PATH}\\cache\\damage_total.jpg"
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}