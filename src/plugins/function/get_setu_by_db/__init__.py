'''
Author: 七画一只妖
Date: 2022-06-03 14:35:38
LastEditors: 七画一只妖
LastEditTime: 2022-06-03 15:29:14
Description: file content
'''
import random


from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from tool.find_power.format_data import is_level_S


from .user_function import get_image
from .user_database import find_user_speak


A_CONT = 65000
S_CONT = 100000


SETU_DATABASE = {
    "A":[
        "image_a_1_500",
        "image_a_2_500",
        "image_a_3_500",
        "image_a_4_500"
    ],
    "S":[
        "image_s_1_500",
        "image_s_2_500",
        "image_s_3_500",
        "image_s_4_500",
        "image_s_5_500",
        "image_s_6_500",
        "image_s_7_500",
        "image_s_8_500",
        "image_s_9_500",
    ]
}


a_get_setu = on_command("等级涩图a")
s_get_setu = on_command("等级涩图s")


@a_get_setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = str(event.group_id)

    if not is_level_S(event):
        return
    user_id = str(event.user_id)
    if find_user_speak(user_id) < A_CONT:
        await a_get_setu.send(f"你的发言不足{A_CONT}条，无法使用该指令\n你当前发言数量：{find_user_speak(user_id)}")
        return

    wh = random.choice(SETU_DATABASE["A"])
    image_name, img_path = get_image(wh)
    sex = image_name.split("-")[0]
    image_name = image_name.replace(sex, "")

    message_list = [f"图片名：{image_name}",f"涩涩值：{sex}",f"来自仓库：{wh}",f"[CQ:image,file=file:///{img_path}]"]


    msg_list = []
    for data_msg in message_list:
        data = {
            "type": "node",
            "data": {
                "name": "无名英雄",
                "uin": "2854196310",
                "content": data_msg
            }
        }
        msg_list.append(data)
    await bot.send_group_forward_msg(group_id=group_id, messages=msg_list)


@s_get_setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = str(event.group_id)

    if not is_level_S(event):
        return
    user_id = str(event.user_id)
    if find_user_speak(user_id) < S_CONT:
        await a_get_setu.send(f"你的发言不足{S_CONT}条，无法使用该指令\n你当前发言数量：{find_user_speak(user_id)}")
        return

    wh = random.choice(SETU_DATABASE["S"])
    image_name, img_path = get_image(wh)
    sex = image_name.split("-")[0]
    image_name = image_name.replace(sex, "")

    message_list = [f"图片名：{image_name}",f"涩涩值：{sex}",f"来自仓库：{wh}",f"[CQ:image,file=file:///{img_path}]"]


    msg_list = []
    for data_msg in message_list:
        data = {
            "type": "node",
            "data": {
                "name": "无名英雄",
                "uin": "2854196310",
                "content": data_msg
            }
        }
        msg_list.append(data)
    await bot.send_group_forward_msg(group_id=group_id, messages=msg_list)