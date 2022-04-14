'''
Author: 七画一只妖
Date: 2022-03-26 12:10:19
LastEditors: 七画一只妖
LastEditTime: 2022-04-14 20:35:06
Description: file content
'''
import json
import os
import random

from .user_database import *

# 获取当前文件路径
current_path = os.path.dirname(os.path.abspath(__file__))

# buff数据文件
buff_data_file = f"{current_path}/data/buff_data.json"


# 根据id查询buff数据
def get_buff_data(buff_id:str) -> dict:
    with open(buff_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if item['bf_id'] == buff_id:
                return item


# 获取用户当前buff
def get_user_buff(user_id:str) -> list:
    # 判断user_id是否存在
    if not is_user_buff_exist(user_id):
        insert_user_buff(user_id)

    # 查询用户buff
    re:list = query_user_buff(user_id)
    user_buff_now = []
    user_buff_list_index = 0
    for i in range(0,len(re)):
        if i == 0:
            user_buff_list_index += 1
            continue
        user_buff_now.append({str(user_buff_list_index):re[i]})
        user_buff_list_index += 1

    # 根据buff计算目前倍率
    final_ak_up, final_am_up = buff_list_multiple(user_buff_now)

    # 打印buff名称
    buff_list_name_lsit = buff_list_name(user_buff_now)


    return final_ak_up, final_am_up, buff_list_name_lsit


# 遍历当前buff的列表累乘倍率
def buff_list_multiple(buff_list:list) -> float:
    final_ak_up = 1.0
    final_am_up = 1.0
    for item in buff_list:
        (key, value), = item.items()
        if value > 0:
            _ = get_buff_data(key)
            final_ak_up *= _['ak_mp']
            final_am_up *= _['am_mp']
    return final_ak_up, final_am_up


# 遍历当前buff的列表，获取对应buff名称，并返回列表
def buff_list_name(buff_list:list) -> list:
    buff_name_list = []
    for item in buff_list:
        (key, value), = item.items()
        if value > 0:
            _ = get_buff_data(key)
            buff_name_list.append({_['bf_name']:value})
    return buff_name_list


# 攻击后，自己的所有buff和目标的所有buff减少1
def buff_reduce(user_id:str, target_id:str) -> None:
    for i in range(1,9):
        if not is_buff_zero(user_id, str(i)):
            update_user_buff(user_id, str(i), f"{-1}")
        if not is_buff_zero(target_id, str(i)):
            update_user_buff(target_id, str(i), f"{-1}")


# 增加user_id的x回合buff
def buff_add(user_id:str, buff_id:str, buff_round:int) -> None:
    update_user_buff(user_id, buff_id, f"+{buff_round}")