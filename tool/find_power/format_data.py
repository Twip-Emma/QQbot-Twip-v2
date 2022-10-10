'''
Author: 七画一只妖
Date: 2022-01-23 12:47:41
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-10 13:33:45
Description: file content
'''
import os
import json


from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from functools import wraps

from .user_database import get_user_info_new, insert_user_info_new, reduce_user_coin


_PATH = os.path.dirname(__file__)
_FILE_PATH = f"{_PATH}\\data\\power.json"


def _get_data():
    data:dict = json.load(open(_FILE_PATH, 'r', encoding='utf8'))
    level_S:list = data["level_S"]
    level_A:list = data["level_A"]
    ban_user:list = data["ban_user"]
    return level_S, level_A, ban_user


# 权限校验：S
def is_level_S(func):
    @wraps(func)
    async def check_power(*args, **kwargs):
        level_S, _, ban_user = _get_data()
        cost = None
        group_id = None
        for k, v in kwargs.items():
            if k == 'event':
                user_id = str(v.user_id)
                try:
                    group_id = str(v.group_id)
                except:
                    group_id = "x"
                if user_id in ban_user:
                    return
                if group_id not in level_S:
                    return
            if k == "cost":
                cost = v
        if not delete_user_coin(user_id=user_id, cost=cost):
            return
        return await func(*args, **kwargs)
    return check_power


# 权限校验：A
def is_level_A(func):
    @wraps(func)
    async def check_power(*args, **kwargs):
        _, level_A, ban_user = _get_data()
        cost = None
        for k, v in kwargs.items():
            if k == 'event':
                user_id = str(v.user_id)
                try:
                    group_id = str(v.group_id)
                except:
                    group_id = "x"
                if user_id in ban_user:
                    return
                if group_id not in level_A:
                    return
            if k == "cost":
                cost = v
        if not delete_user_coin(user_id=user_id, cost=cost):
            return
        return await func(*args, **kwargs)
    return check_power


# 行动点扣除
def delete_user_coin(user_id:str, cost:int) -> bool:
    user_data = get_user_info_new(user_id=user_id)
    if user_data == None:
        insert_user_info_new(user_id=user_id)
        user_data = get_user_info_new(user_id=user_id)
    if user_data[1] >= cost:
        reduce_user_coin(user_id=user_id, user_coin=cost)
        return True
    else:
        return False
