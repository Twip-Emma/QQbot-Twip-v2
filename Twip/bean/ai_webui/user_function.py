'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-11-27 22:38:30
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-01-30 11:24:59
'''
import json
from pathlib import Path
import requests

from setting import ai_webui

BASE_PATH: str = Path(__file__).absolute().parents[0]


async def get_image(user_ap:str, user_id:str) -> str:
    ap = user_ap
    np = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts,signature, watermark, username, blurry, artist name,bad feet, twintails,"

    payload = {"fn_index": 103,"data": [ap,np,],"session_hash": ""}


    data_a = """{"fn_index": 103,"data": [""" + '"' + ap + ',","' + np + ',",'
    data_b = """"None","None",50,"Euler a","","",1,1,7,-1,-1,0,0,0,"",960,640,"",0.7,0,0,"None",0.9,5,"0.0001","","None","",0.1,"","","","","","","Seed","","Nothing","","","","","","","" """
    data_c = """],"session_hash": ""}"""

    payload = data_a + data_b + data_c

    # print(type(payload))
    a = json.loads(payload)
    # print(type(a))
    header = {
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            }

    r = requests.post(
        f"http://{ai_webui}/run/predict/", data=json.dumps(a), headers=header)
    re_data:dict = r.json()
    # print(re_data["data"][0][0]["name"])
    image_url = f"http://{ai_webui}/file=" + re_data["data"][0][0]["name"]
    res = requests.get(image_url)

    with open(f"{BASE_PATH}\\images\\{user_id}.jpg","wb") as f:
        f.write(res.content)

    return f"{BASE_PATH}\\images\\{user_id}.jpg"
