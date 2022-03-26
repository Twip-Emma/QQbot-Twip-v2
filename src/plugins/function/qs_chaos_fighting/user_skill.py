'''
Author: 七画一只妖
Date: 2022-03-26 13:50:20
LastEditors: 七画一只妖
LastEditTime: 2022-03-26 18:28:35
Description: file content
'''
import json
import os
import random

from .user_database import *

# 获取当前文件路径
current_path = os.path.dirname(os.path.abspath(__file__))

# buff数据文件
skill_data_file = f"{current_path}/data/skill_data.json"


# 根据skill_id获取skill数据
def get_skill_data(skill_id:str) -> dict:
    with open(skill_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if item['skill_id'] == skill_id:
                return item


# 根据skill_name获取skill数据
def get_skill_data_by_name(skill_name:str) -> dict:
    with open(skill_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if item['skill_name'] == skill_name:
                return item