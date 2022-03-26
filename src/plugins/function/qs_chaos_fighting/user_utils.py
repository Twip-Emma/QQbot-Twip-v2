'''
Author: 七画一只妖
Date: 2022-03-25 18:23:57
LastEditors: 七画一只妖
LastEditTime: 2022-03-26 18:28:38
Description: file content
'''
import json
import os
import random

from .user_database import *

# 获取当前文件路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 武器数据文件
weapon_data_file = f"{current_path}/data/arms_data.json"


# 随机生成新用户的属性
def generate_user_attribute():
    # 生成随机数
    user_health = random.randint(5000, 10000)
    user_armor = random.randint(30, 50)
    user_attack = random.randint(70, 100)
    return user_health, user_armor, user_attack


# 根据ID获取武器数据
def get_weapon_data(weapon_id:str) -> dict:
    with open(weapon_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if item['id'] == weapon_id:
                return item


# 随机抽取一件武器
def get_random_weapon() -> dict:
    with open(weapon_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return random.choice(data)


# 根据user_id获取用户的生命值、护甲值、攻击力
def get_user_attribute(user_id:str) -> tuple:
    ###############################################################
    # 用户基本数据
    # 先判断用户是否存在
    if not is_user_exist(user_id):
        #新建用户
        insert_user(user_id, *generate_user_attribute())

    # 如果用户存在，则查询用户属性
    re = query_user_attribute(user_id)

    ###############################################################
    # 武器方面
    # 判断user_arms中user_id是否存在
    if not is_user_arms_exist(user_id):
        # 新建用户武器
        insert_user_arms(user_id)
    # 查询用户武器
    user_arms:list = query_user_arms(user_id)
    # 遍历user_arms，每两项为一组，分别为武器id和武器等级，生成一个字典
    user_arms_dict = []
    user_arms_dict_index = 0
    for i in range(0, len(user_arms)):
        if i == 0:
            continue
        if user_arms_dict_index % 2 == 0:
            # 列表添加一个元素
            user_arms_dict.append({user_arms[user_arms_dict_index+1]: user_arms[user_arms_dict_index + 2]})
        user_arms_dict_index += 1    
    # 遍历user_arms_dict，key是武器id，value是武器等级
    # 将key传给get_weapon_data()，获取武器数据
    ex_hp = 0
    ex_ak = 0
    ex_am = 0
    for item in user_arms_dict:
        (key, value), = item.items()
        if key == None or value == None:
            continue
        _ = get_weapon_data(key)
        ex_hp += _['hp_start'] + value * _['hp_up']
        ex_ak += _['ak_start'] + value * _['ak_up']
        ex_am += _['am_start'] + value * _['am_up']


    # 输出用户属性，算上ex_hp, ex_ak, ex_am
    # print(f"用户ID：{user_id}")
    # print(f"用户生命值：{re[1]} + {ex_hp} = {re[1] + ex_hp}")
    # print(f"用户护甲值：{re[2]} + {ex_am} = {re[2] + ex_am}")
    # print(f"用户攻击力：{re[3]} + {ex_ak} = {re[3] + ex_ak}")
    return re[1] + ex_hp, re[2] + ex_am, re[3] + ex_ak