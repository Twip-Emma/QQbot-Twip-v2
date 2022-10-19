'''
Author: 七画一只妖
Date: 2021-09-22 19:01:07
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-19 15:27:58
Description: file content
'''
from os import path

import MySQLdb

THIS_PATH = path.join(path.dirname(__file__))
from setting import *


gacha_dict = [
{"total":500,"time":0},
{"total":750,"time":5},
{"total":999991,"time":10},
{"total":999992,"time":10},
{"total":999993,"time":10},
{"total":999994,"time":10},
{"total":999995,"time":10},
{"total":999996,"time":10},
{"total":999997,"time":10}
]


def find_user_gacha_time(user_id):
    time = 0
    total = find_user_speak_total(user_id)
    for item in gacha_dict:
        if total < item["total"]:
            time = item["time"]
            break
    return time, item["total"], total


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
