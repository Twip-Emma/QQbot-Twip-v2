'''
Author: 七画一只妖
Date: 2022-06-03 14:35:38
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-24 15:22:30
Description: file content
'''
import random

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_S

from .user_function import get_image

__plugin_meta__ = PluginMetadata(
    name='涩图-数据库',
    description='获取一张涩图、消耗健康值，健康值越低图片黑域越多',
    usage='''等级涩图a/等级涩图s''',
    extra={'version': 'v1.0.0',
           'cost': '25/75'}
)

SETU_DATABASE = {
    "A": [
        "image_a_1_500",
        "image_a_2_500",
        "image_a_3_500",
        "image_a_4_500"
    ],
    "S": [
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


a_get_setu = on_command("等级涩图a", block=True, priority=2)
s_get_setu = on_command("等级涩图s", block=True, priority=2)


@a_get_setu.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost = 25):
    group_id = str(event.group_id)
    user_id = str(event.user_id)

    wh = random.choice(SETU_DATABASE["A"])
    image_name, img_path, user_health = get_image(wh, user_id)
    sex = image_name.split("-")[0]
    image_name = image_name.replace(sex, "")

    message_list = [f"图片名：{image_name}", f"涩涩值：{sex}", f"来自仓库：{wh}",
                    f"[CQ:image,file=file:///{img_path}]", f"您剩余健康值：{user_health}"]

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
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost = 75):
    group_id = str(event.group_id)
    user_id = str(event.user_id)

    wh = random.choice(SETU_DATABASE["S"])
    image_name, img_path, user_health = get_image(wh, user_id)
    sex = image_name.split("-")[0]
    image_name = image_name.replace(sex, "")

    message_list = [f"图片名：{image_name}", f"涩涩值：{sex}", f"来自仓库：{wh}",
                    f"[CQ:image,file=file:///{img_path}]", f"您剩余健康值：{user_health}"]

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
