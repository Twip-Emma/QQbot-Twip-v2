'''
Author: 七画一只妖
Date: 2022-09-04 19:53:01
LastEditors: 七画一只妖
LastEditTime: 2022-09-04 20:14:34
Description: file content
'''
from typing import Union
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent
import requests


from bs4 import BeautifulSoup


ele_power_finder = on_command("电费", block=True, priority=2)

URL_1 = "http://39.108.173.72:8080/isimshngc/loginServlet"

URL_2 = "http://39.108.173.72:8080/isimshngc/monServlet?monType=0"


@ele_power_finder.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    msg = str(event.get_message()).split()
    try:
        if str(event.group_id) not in ["274733672","571670250"]:
            return
    except:
        pass

    if len(msg) == 1:
        payload = {
            "xiaoquId": 1,
            "buildingId": 362,
            "roomName": 307
        }
        await ele_power_finder.send(message=f"滨江9307电费总余量{get_data(payload)}度")
    else:
        return


def get_data(payload):
    s = requests.Session()
    s.post(url=URL_1, data=payload, verify=False)
    resp = s.get(url=URL_2, verify=False)
    resp.encoding = "utf-8"

    s = BeautifulSoup(resp.text, 'html.parser')
    power = s.find_all("div", class_="content1")[0].get_text()
    return power


# print(get_data({
#     "xiaoquId": 1,
#     "buildingId": 362,
#     "roomName": 307
# }))
