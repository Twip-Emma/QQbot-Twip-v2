'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-06 23:32:24
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-08 10:44:52
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import httpx
# import asyncio
# from .cookies import header

# from cookies import header


# 全局变量下标
req_index = 0

# 记得填
COOKIES = "i-wanna-go-back=-1; buvid_fp_plain=undefined; blackside_state=0; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO2916589792625841; DedeUserID=178547325; DedeUserID__ckMd5=d90ee02c8bad0cdd; buvid4=23F4DCF0-243F-05CD-0C32-458841A6D0A778370-022071818-OsDwyx78W%2ByrNhIDcatWKA%3D%3D; rpdid=|(m~Y|~~|~l0J'uYY)l~uu)l; is-2022-channel=1; hit-new-style-dyn=1; dy_spec_agreed=1; CURRENT_PID=0507da70-c954-11ed-b885-5544c605f9c2; FEED_LIVE_VERSION=V8; home_feed_column=5; buvid3=7E1CE2B0-09B1-38D0-C6CC-6F35C6A1603546445infoc; b_nut=1689678846; _uuid=A95CADCE-C543-3475-D712-102410C1ED869746942infoc; header_theme_version=CLOSE; nostalgia_conf=-1; hit-dyn-v2=1; Hm_lvt_7999812113dc28f5de372c8e8109efc4=1690549050; CURRENT_QUALITY=80; fingerprint=d3f0ed712f1dc1e49fa63fb6757c26e9; CURRENT_FNVAL=4048; browser_resolution=1528-742; SESSDATA=2552b3c6%2C1712120101%2C2c109%2Aa1CjBr1uCOGqfkU2SkCvF3i32CwXca8CBsgTSoCBTl5MuGyWIeSz8FV2bQLDJ27sNiIG0SVnNMQXQySU1lRzVTemNoSWdYcFBRalNzNVJGQU44Tk84RnR2UlotQjc4OHJ0QWNrRW93M2VCR3p4TDhNRHQxVUZxLW9VS1ltT0xUTEFSdDU5THcyRUdBIIEC; bili_jct=4c06c5ddbeed1bc26674fc0c7fe472dd; PVID=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY4NTk5MjgsImlhdCI6MTY5NjYwMDY2OCwicGx0IjotMX0.Hh4tDG2AAd5GPvA07JXNqUeZ3pQkR6ssNs2JK6vEvVc; bili_ticket_expires=1696859868; bp_video_offset_178547325=849676824754520100; buvid_fp=d3f0ed712f1dc1e49fa63fb6757c26e9"

SECRET_KEY = "192f4699782268107f37e8bd117812f"

DATE_URL = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report_date?ts=1696605833368&nonce=75eb6ddb-ddf9-4d57-9a77-b81a4f497f8a&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=d516800de7bbb7d860642a7e64aa0fcf"
DAILY_URL = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?ts=1696605833457&nonce=270389f7-01e1-447b-874b-a57dfea83754&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign=e3fbe1f86dbcc76d49a8178f9dd81fc6"
DAILY_URL_TAR_A = f"https://api.game.bilibili.com/game/player/tools/kan_gong/fight_report?date="
DAILY_URL_TAR_B = f"&ts=&nonce=&appkey=a5e793dd8b8e425c9bff92ed79e4458f&sign="
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

# 合法的请求参数
REQ_TABLE = [
    {
        "ts": "1696729989816",
        "nonce": "e7c2ba80-a9e0-4355-919c-45f37adf5a2b",
        "sign": "e1d4c8acd589d125cc73be09330e1222"
    },
    {
        "ts": "1696732349598",
        "nonce": "a3fc6348-9f49-4f54-86c5-fec0de4b86eb",
        "sign": "efe23d026abacc7c0859697da4a1bef8"
    },
    {
        "ts": "1696732366859",
        "nonce": "fa0db6a2-b98d-4b4e-b2c2-535f022b1c2d",
        "sign": "7d924c4c05ece993c3ed7a7a487488aa"
    },
    {
        "ts": "1696732384363",
        "nonce": "5b74d7f6-a9e1-4890-b8c6-585fb1f65f07",
        "sign": "c8c6aa86a710e2c8375d1dbd7729b1b7"
    },
    {
        "ts": "1696732402459",
        "nonce": "3b9d65b5-7117-4483-812b-82c377d98449",
        "sign": "dee2b6cb50f2cccf5632f51bcb798627"
    },
    
]


# 获取日期
async def get_date():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DATE_URL, headers=header)
            re_data: dict = r.json()
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def get_daily():
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url=DAILY_URL, headers=header)
            re_data: dict = r.json()
            return re_data
    except Exception as e:
        print(e)
        return {"code": 500,
                "message": "error"}
    

async def get_daily_target(date: str):
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            url = change_req(DAILY_URL_TAR_A + date + DAILY_URL_TAR_B)
            r = await client.get(url=url, headers=header)
            re_data: dict = r.json()
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
    

# 替换nonce 和sign
def change_req(req_url:str) -> str:
    global req_index

    req_url = req_url.replace("ts=", "ts=" + REQ_TABLE[req_index]['ts'])
    req_url = req_url.replace("nonce=", "nonce=" + REQ_TABLE[req_index]['nonce'])
    req_url = req_url.replace("sign=", "sign=" + REQ_TABLE[req_index]['sign'])

    req_index += 1
    if req_index > len(REQ_TABLE) - 1:
        req_index = 0

    return req_url


