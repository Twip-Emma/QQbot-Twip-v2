'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:55:54
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-06-24 13:09:44
'''
import json


def load_data(path: str) -> dict:
    return json.load(open(path, 'r', encoding='utf8'))


def save_data(path: str, data: dict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


def data_format(data):
    for item in data["info"]:
        for d_item in item["damage_list"]:
            d_item["boss_name"] = _data_format(d_item["boss_name"])
    return data


def _data_format(name):
    data = {
        "恶魔首领":"恶魔",
        "暗影魔王":"暗影",
        "boss_harvester_guild_fury":"蚊子",
        "boss_graboid_guild_fury":"沙虫",
        "boss_nine_tailed_fox_guild":"佳岚",
        "boss_robot_knight_new_guild":"大锤",
        "boss_minister_guild":"邓肯",
        "雪人将军盖斯特":"雪人",
        "九尾狐佳岚":"佳岚",
        "宰相邓肯":"邓肯",
        "帝国骑士":"骑士",
        "雪人将军盖斯特":"雪人",
        "妖精":"妖精",
        "春秋派首领":"春秋",
        "哥布林族长":"族长",
        "侵略军司令官":"司令",
        "boss_mech_guild_fury_43th":"熊猫",
        "boss_admiral_guild_43th_modified":"船长",
        "boss_portrait_guild_43th":"画像",
        "boss_invader_director_guild":"导演",
        "机械人艾瑞娜":"奶奶",
        "愤怒的牛头人":"牛头",
        "熔岩史莱姆国王":"史莱姆"
    }
    return data[name]