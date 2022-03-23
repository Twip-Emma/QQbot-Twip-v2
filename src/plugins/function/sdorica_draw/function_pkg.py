'''
Author: 七画一只妖
Date: 2022-03-16 18:58:50
LastEditors: 七画一只妖
LastEditTime: 2022-03-23 21:39:23
Description: file content
'''
import random

from .get_image import get_png_path

import os
from os import path
import json
import copy


FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# 概率设置
GOLD = 30
PURPLE = 90
BLUE = 200

# 卡池映射
POOL_INFO_RANK = {
    "起源十连": ["sp角色", "2阶角色", "1阶角色", "0阶角色"],
    "盛夏十连": ["mz角色", "2阶角色", "1阶角色", "0阶角色"],
    "限定十连": ["特殊角色", "2阶角色", "1阶角色", "0阶角色"],
    "首发十连": ["3阶角色", "2阶角色", "1阶角色", "0阶角色"],
    "群友十连": ["群友角色", "2阶角色", "1阶角色", "0阶角色"],
}

# 导入pool_info.json
def load_pool_info():    
    # 获取char文件夹内的所有图片
    char_pool = {}
    for file in os.listdir(FILE_PATH + "/char"):
        char_pool[file] = []
        for file2 in os.listdir(FILE_PATH + "/char/" + file):
            if file2.endswith(".png"):
                file2 = file2.replace(".png", "")
                char_pool[file].append(file2)
    return char_pool


# 根据卡池类型进行抽卡
def get_pool_info(pool_name):
    pool_info = POOL_INFO_RANK[pool_name]
    if pool_info == None:
        return None

    # 载入卡池
    char_pool = load_pool_info()

    char_list = []
    char_name_list = []

    x = 0
    while x < 10:
        flag = random.randint(0, 1000)
        if flag <= GOLD:
            a = random.choice(char_pool[POOL_INFO_RANK[pool_name][0]])
        elif flag <= PURPLE:
            a = random.choice(char_pool[POOL_INFO_RANK[pool_name][1]])
        elif flag <= BLUE:
            a = random.choice(char_pool[POOL_INFO_RANK[pool_name][2]])
        else:
            a = random.choice(char_pool[POOL_INFO_RANK[pool_name][3]])
        char_name_list.append(a)

        a = get_png_path(a)
        char_list.append(a)
        x += 1

    return char_list, char_name_list


# 去重函数，传入角色+等阶的列表，返回一个是否为new的0/1列表
# 0是new，1是重复
def removal1(char_name_list):
    is_new = ["0","0","0","0","0","0","0","0","0","0"] # 定义0、1列表
    x = 0 # 扫描的索引值
    char_name_list_p = copy.deepcopy(char_name_list)
    for char in char_name_list:
        char_name_list_p[x] = "==="
        y = 0
        for item in char_name_list_p:
            if item == char:
                is_new[y] = "1"
            y += 1
        x += 1
    return is_new


# 十连保底蓝
def ten_blue():
    char_pool = load_pool_info()
    return random.choice(char_pool["1阶角色"]) 