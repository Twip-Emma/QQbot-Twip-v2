'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-06 23:32:24
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-07 20:08:36
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import httpx
# import asyncio
# from .cookies import header

# from cookies import header


DATE_URL = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report_date?ts=1696605833368&nonce=75eb6ddb-ddf9-4d57-9a77-b81a4f497f8a&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=d516800de7bbb7d860642a7e64aa0fcf"
DAILY_URL = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?ts=1696605833457&nonce=270389f7-01e1-447b-874b-a57dfea83754&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=e3fbe1f86dbcc76d49a8178f9dd81fc6"
DAILY_URL_TAR_A = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?date="
DAILY_URL_TAR_B = f"&ts=1696644412590&nonce=1ce27678-61f6-4a91-9ad8-10dad1d2010d&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=ad94b01a3d3000f40abdc2e8b986a18d"
RATE_URL = f"""https://api.game.bilibili.com/game/player/tools/kan_gong/fight_news?ts=1687583171294&nonce=286263db-9437-493f-bc4f-25ec6b1326ee&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=73bb681870500d80828ec38ebf751bbc"""


from Twip import KGQGJ_COOKIE

header = {
    "accept": f"text/htfml,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": f"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "connection": f"keep-alive",
    "cookie": KGQGJ_COOKIE
}


header2 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
    "connection": "keep-alive",
    "cookie": KGQGJ_COOKIE
}

# 获取日期
async def get_date():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DATE_URL, headers=header)
            re_data: dict = r.json()
            # print(re_data['data']['dates'])
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def get_daily():
    # date_list = await get_date()

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAILY_URL, headers=header)
            re_data: dict = r.json()
            # print(re_data['data'])
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def get_daily_target(date: str):
    # date_list = await get_date()

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAILY_URL_TAR_A + date + DAILY_URL_TAR_B, headers=header)
            re_data: dict = r.json()
            # print(re_data['data'])
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500, 
                "message": "error" }
    

async def get_rate_data():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=RATE_URL, headers=header)
            re_data: dict = r.json()
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    


# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_daily())
    

