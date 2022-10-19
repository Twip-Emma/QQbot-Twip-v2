'''
Author: 七画一只妖
Date: 2021-09-09 18:36:14
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-19 15:28:24
Description: file content
'''
import json
import datetime
import os

from .database import *


# 抽卡次数判断
PATH = os.path.dirname(__file__)
SIGN_PATH = f"{PATH}\\data\\sign_time.json"
PACK_PATH = f"{PATH}\\data\\user_package.json"


# 抽卡限制判断
def attack_chack(user_id):
    # 返回理应抽卡次数
    time, total, sptotal = find_user_gacha_time(user_id)
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
            return False, time, total, sptotal
        else:
            return True, time, total, sptotal
    
    # 当天抽卡次数小于等于0，则不允许抽卡
    if sign[user_id]["sign_time"] == sign_time:
        if sign[user_id]["gacha_time"] <= 0:
            return False, time, total, sptotal
        else:
            sign[user_id]["gacha_time"] -= 1
            with open(SIGN_PATH, 'w', encoding='utf-8') as f:
                f.write(json.dumps(sign, ensure_ascii=False))
                f.close() 
            return True, time, total, sptotal
    else:
        sign[user_id]["sign_time"] = sign_time
        sign[user_id]["gacha_time"] = time - 1
        with open(SIGN_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(sign, ensure_ascii=False))
            f.close() 
        if time == 0:
            return False, time, total, sptotal
        else:
            return True, time, total, sptotal


# 根据用户魂册去重
# 传入：角色+阶数列表，已经过第一次去重的0/1列表，用户QQ
# 传出：新的0/1列表
def select_user_pack(char_name_list,is_new,user_id):
    # print("第二次去重的角色列表：",char_name_list)
    data = json.load(open(PACK_PATH, 'r', encoding='utf8'))

    # 判断是否为新用户
    if user_id not in data:
        new_boj = {user_id : {}}
        data.update(new_boj)

    x = 0 
    for name in char_name_list:
        char_info = name.split("-")
        real_name = char_info[0]
        # char_frame = char_info[1]

        # 根据阶数判断碎片增加量
        char_frame = 0
        if"SP" in name or"3阶" in name or"X阶" in name:
            char_frame = 50
        elif"2阶" in name:
            char_frame = 20
        elif"1阶" in name:
            char_frame = 5
        elif"0阶" in name:
            char_frame = 1


        # 读取用户仓库以便于判断是不是new
        if real_name in data[user_id]:
            is_new[x] = "1"
            data[user_id][real_name] += char_frame
        elif real_name not in data[user_id]:
            new_obj = {real_name:char_frame}
            data[user_id].update(new_obj)
        x += 1

    
    with open(PACK_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close() 
    # print("第二次去重",is_new)
    return is_new
