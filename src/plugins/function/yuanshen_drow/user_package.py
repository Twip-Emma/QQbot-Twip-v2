'''
Author: 七画一只妖
Date: 2021-09-09 18:36:14
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 16:48:10
Description: file content
'''
import json
import datetime
import os

from .database import *


# 抽卡次数判断
PATH = os.path.dirname(__file__)
SIGN_PATH = f"{PATH}\\data\\sign_time.json"


# 抽卡限制判断
def attack_chack(user_id):
    time = find_user_gacha_time(user_id)
    # time = 999
    sign:dict = json.load(open(SIGN_PATH, 'r', encoding='utf8'))
    sign_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # 如果没有这个人，则新建用户
    if user_id not in sign:
        sign_obj = {user_id:{"sign_time":sign_time,"gacha_time":time}}
        sign.update(sign_obj)
        with open(SIGN_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(sign, ensure_ascii=False))
            f.close() 
        if time == 0:
            return False
        else:
            return sign[user_id]["gacha_time"]
    
    # 当天抽卡次数小于等于0，则不允许抽卡
    if sign[user_id]["sign_time"] == sign_time and sign[user_id]["gacha_time"] <= 0:
        return False
    # 当天抽卡次数大于0，可以抽卡
    elif sign[user_id]["sign_time"] == sign_time and sign[user_id]["gacha_time"] > 0:
        sign[user_id]["gacha_time"] -= 1
        with open(SIGN_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(sign, ensure_ascii=False))
            f.close() 
        return sign[user_id]["gacha_time"]
    # 新的一天抽卡
    elif sign[user_id]["sign_time"] != sign_time:
        sign[user_id]["sign_time"] = sign_time
        sign[user_id]["gacha_time"] = time - 1
        with open(SIGN_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(sign, ensure_ascii=False))
            f.close() 
        if time == 0:
            return False
        else:
            return sign[user_id]["gacha_time"]