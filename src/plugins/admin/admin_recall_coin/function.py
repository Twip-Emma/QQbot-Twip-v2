'''
Author: 七画一只妖
Date: 2022-03-12 19:48:14
LastEditors: 七画一只妖
LastEditTime: 2022-03-12 20:01:32
Description: file content
'''
import json
from os import path

THIS_PATH = path.join(path.dirname(__file__))
COIN_PATH = THIS_PATH + "\\coin.json"


def get_user_coin() -> int:
    data:dict = json.load(open(COIN_PATH, 'r', encoding='utf8'))
    return data["user_coin"]


def save_new_coin(new_coin:int) -> None:
    data:dict = json.load(open(COIN_PATH, 'r', encoding='utf8'))
    data["user_coin"] = new_coin
    with open(COIN_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()



def coin_up(count:int) -> int:
    now = get_user_coin()
    now += count
    save_new_coin(now)
    return now


def coin_down(count:int) -> int:
    now = get_user_coin()
    now -= count
    save_new_coin(now)
    return now