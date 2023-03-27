'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:55:54
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-03-27 14:41:19
'''
import json


def load_data(path: str) -> dict:
    return json.load(open(path, 'r', encoding='utf8'))


def save_data(path: str, data: dict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


def data_format(data):
    for item in data:
        for d_item in item["damage_list"]:
            d_item["boss_name"] = _data_format(d_item["boss_name"])
    return data


def _data_format(name):
    data = {
        "恶魔首领":"恶魔",
        "暗影魔王":"暗影",
        "boss_harvester_guild_fury":"蚊子",
        "boss_graboid_guild_fury":"沙虫",
    }
    return data[name]