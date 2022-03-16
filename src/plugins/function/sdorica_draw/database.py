'''
Author: 七画一只妖
Date: 2021-09-22 19:01:07
LastEditors: 七画一只妖
LastEditTime: 2022-03-16 21:30:53
Description: file content
'''
from os import path
import sqlite3

import MySQLdb

THIS_PATH = path.join(path.dirname(__file__))
from tool.setting.database_setting import *


gacha_dict = [
{"total":500,"time":0},
{"total":1000,"time":2},
{"total":2000,"time":4},
{"total":5000,"time":6},
{"total":10000,"time":8},
{"total":20000,"time":10},
{"total":50000,"time":12},
{"total":80000,"time":14},
{"total":110000,"time":16}
]


def find_user_gacha_time(user_id):
    time = 0
    total = find_user_speak_total(user_id)
    for item in gacha_dict:
        if total < item["total"]:
            time = item["time"]
            break
    return time


def chack_user_gacha(user_id):
    time = 0
    total = find_user_speak_total(user_id)
    for item in gacha_dict:
        if total < item["total"]:
            time = item["time"]
            break
        
    return f"""【Error】你的发言小于{item["total"]},有{time}次抽卡机会，现已用完\n你的发言总数：{total}"""


def find_user_speak_total(user_id):
    sql = f"""
            select * from user_info where user_id='{user_id}';
    """
    re = sql_dql(sql)
    total = re[0][4]
    return total


### 数据库封装
def sql_dql(sql):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result
