'''
Author: 七画一只妖
Date: 2022-03-23 20:34:57
LastEditors: 七画一只妖
LastEditTime: 2022-03-23 21:33:29
Description: file content
'''

import os
import json


# 检索万象物语抽卡的路径（sdorica_draw文件夹）
# 拼接路径
PACK_PATH = f"src\\plugins\\function\\sdorica_draw"

# 用户魂册
USER_PACK_PATH = f"{PACK_PATH}\\data\\user_package.json"

# 现有的角色池（文件夹）路径
ROLE_POOL_PATH = f"{PACK_PATH}\\char"


# 计算ROLE_POOL_PATH下的文件及其子孙文件夹内有多少个图片
def get_role_pool_num():
    role_pool_num = 0
    for root, dirs, files in os.walk(ROLE_POOL_PATH):
        for file in files:
            if file.endswith(".png"):
                role_pool_num += 1
    return role_pool_num
    

# 传入一个字典，key是角色名，value是角色碎片，遍历所有角色，计算value是否超过225，如果超过225，则写作225，否则不变
# 返回一个字典，key是角色名，value是比例
def get_role_pool_num_ratio(role_pool_num_dict):
    for key in role_pool_num_dict:
        if role_pool_num_dict[key] > 225:
            role_pool_num_dict[key] = 225
    # 累加这些value
    total = 0
    for key in role_pool_num_dict:
        total += role_pool_num_dict[key]
    total_flag = get_role_pool_num() *225
    # 计算total 和 total_flag的比例，并保留两位小数
    return round((total / total_flag)*100, 2)


# 根据传入的user_id，在USER_PACK_PATH里面查找对应的字典并返回
def get_user_package(user_id):
    with open(USER_PACK_PATH, "r", encoding="utf-8") as f:
        user_package = json.load(f)
    return user_package[user_id]


# 传入user_id，返回练度比例
def get_user_package_ratio(user_id):
    user_package = get_user_package(user_id)
    return get_role_pool_num_ratio(user_package)


# 传入user_id，返回图鉴比例
def get_user_package_book_ratio(user_id):
    user_package_count = len(get_user_package(user_id))
    return round((user_package_count / get_role_pool_num())*100, 2)