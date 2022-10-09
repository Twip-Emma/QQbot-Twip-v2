'''
Author: 七画一只妖
Date: 2022-09-04 19:53:01
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 15:59:10
Description: file content
'''
from typing import Union

import requests
from bs4 import BeautifulSoup
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent,
                                         PrivateMessageEvent)
from nonebot.plugin import PluginMetadata

from tool.utils.logger import logger as my_logger

__plugin_meta__ = PluginMetadata(
    name='电费查询',
    description='查询湖南工程学院指定宿舍的电费',
    usage='''电费 <滨江|学海|亲民|明德> <宿舍号>''',
    extra={'version': 'v1.0.0',
           'cost': '###0'}
)


ele_power_finder = on_command("电费", block=True, priority=2)

URL_1 = "http://39.108.173.72:8080/isimshngc/loginServlet"

URL_2 = "http://39.108.173.72:8080/isimshngc/monServlet?monType=0"


@ele_power_finder.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent],bot:Bot):
    msg = str(event.get_message()).split()
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    # await get_luck.finish("hi")
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    if len(msg) == 1:
        payload = {
            "xiaoquId": 1,
            "buildingId": 362,
            "roomName": 307
        }
        await ele_power_finder.send(message=f"（默认查询）滨江9307电费总余量{get_data(payload)}度")
    elif "滨江" in msg[1]:
        room_id = msg[1][-3:]
        buildId = msg[1][2:-3]
        buildId_dict = {"1": 2,
                        "2": 3,
                        "3": 4,
                        "4": 5,
                        "5": 6,
                        "6": 7,
                        "7": 8,
                        "8": 361,
                        "9": 362,
                        "10": 609,
                        "11": 610}
        # print(f'{buildId}棟{room_id}间')
        payload = {
            "xiaoquId": 1,
            "buildingId": buildId_dict[buildId],
            "roomName": room_id
        }
        await ele_power_finder.send(message=f"滨江{buildId}栋{room_id}电费总余量{get_data(payload)}度")
    elif "亲民" in msg[1]:
        room_id = msg[1][-3:]
        buildId = msg[1][2:-3]
        buildId_dict = {"1": 52,
                        "2": 53,
                        "3": 54,
                        "4": 55,}
        # print(f'{buildId}棟{room_id}间')
        payload = {
            "xiaoquId": 51,
            "buildingId": buildId_dict[buildId],
            "roomName": room_id
        }
        await ele_power_finder.send(message=f"亲民{buildId}栋{room_id}电费总余量{get_data(payload)}度")
    elif "学海" in msg[1]:
        room_id = msg[1][-3:]
        buildId = msg[1][2:-3]
        buildId_dict = {"1": 141,
                        "2": 142,
                        "3": 143,
                        "4": 144,
                        "5": 145,
                        "6": 146,
                        "7": 147,
                        "8": 148,
                        "9": 149,
                        "10": 150,
                        "11": 151}
        # print(f'{buildId}棟{room_id}间')
        payload = {
            "xiaoquId": 140,
            "buildingId": buildId_dict[buildId],
            "roomName": room_id
        }
        await ele_power_finder.send(message=f"学海{buildId}栋{room_id}电费总余量{get_data(payload)}度")
    elif "明德" in msg[1]:
        room_id = msg[1][-3:]
        buildId = msg[1][2:-3]
        buildId_dict = {"1": 80,
                        "2": 81,
                        "3": 82,
                        "4": 83,
                        "5": 84,
                        "6": 85,
                        "7": 86,
                        "8": 87,
                        "9": 88,
                        "10": 89,}
        # print(f'{buildId}棟{room_id}间')
        payload = {
            "xiaoquId": 51,
            "buildingId": buildId_dict[buildId],
            "roomName": room_id
        }
        await ele_power_finder.send(message=f"明德{buildId}栋{room_id}电费总余量{get_data(payload)}度")
    else:
        await ele_power_finder.send("目前只支持：滨江|明德|学海|亲民\n请输入正确的宿舍例如：\n电费 滨江9307")
    my_logger.success(
        '电费查询', f'成功发送：用户：<m>{recall_user_name}{user_id}</m> | 群：<m>{group_id}</m>')


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
