'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:05:56
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-04-14 23:08:59
FilePath: \060坎公骑冠剑会战工具\function.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
from pathlib import Path
import requests
import httpx

from .setting import DAMAGE_URL, RATE_URL, DAO_IMAGE, DAO_DAILY, DAMAGE_TOTAL
from .cookies import header, header2
from .utils.data_utils import save_data

BASE_PATH: str = Path(__file__).absolute().parents[0]


async def f_get_user_data(date:str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAMAGE_URL + date, headers=header)
            re_data: dict = r.json()
            save_data(f"{BASE_PATH}\\data\\user_data.json", re_data)
            data = re_data["data"]
            return data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}


async def f_get_damage_data(date:str):
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAMAGE_URL + date, headers=header)
            re_data: dict = r.json()
            save_data(f"{BASE_PATH}\\data\\damage_data.json", re_data)
            data = re_data["data"]
            return data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}


async def f_get_rate_data():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=RATE_URL, headers=header)
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