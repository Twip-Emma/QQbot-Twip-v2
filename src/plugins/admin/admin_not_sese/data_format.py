'''
Author: 七画一只妖
Date: 2022-05-30 16:10:58
LastEditors: 七画一只妖
LastEditTime: 2022-05-30 17:51:45
Description: file content
'''
import json
import os
import datetime


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE_PATH, 'user_info.json')
LEVEL = os.path.join(BASE_PATH, 'level.json')


# 获取用户信息，返回一个字典
def get_user_info(user_id):
    # 读取用户信息
    with open(DATA, 'r') as f:
        user_info = json.load(f)
    # 返回用户信息
    return user_info[user_id]


# 获取当前时间
def get_now_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return now_time


# 用户签到成功
def sign_success(user_id):
    with open(DATA, 'r') as f:
        data = json.load(f)
    data[user_id]['exp'] += data[user_id]['days']
    data[user_id]['sign'] = get_now_time()
    data[user_id]['days'] += 1
    with open(DATA, 'w') as f:
        json.dump(data, f)


# 签到
def sign_in(user_id):
    # 获取当前时间
    now_time = get_now_time()
    # 获取用户信息
    user_info = get_user_info(user_id)


    # 判断用户是否签到
    if user_info['sign'] == now_time:
        return '你今天已签到'
    else:
        sign_success(user_id)
        return '签到成功'


# 获取值
def get_value(user_id):
    user_info = get_user_info(user_id)
    exp = user_info['exp']
    # 遍历LEVEL的键值对
    with open(LEVEL, 'r') as f:
        data = json.load(f)
    for key, value in data.items():
        if exp < int(key):
            return value
    return value
        
    

print(get_value('1157529280'))