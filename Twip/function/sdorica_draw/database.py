'''
Author: 七画一只妖
Date: 2021-09-22 19:01:07
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-01-06 19:42:52
Description: file content
'''
from os import path

import MySQLdb

THIS_PATH = path.join(path.dirname(__file__))
from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB


gacha_dict = [
{"total":500,"time":0},
{"total":750,"time":5},
{"total":999991,"time":99},
{"total":999992,"time":99},
{"total":999993,"time":99},
{"total":999994,"time":99},
{"total":999995,"time":99},
{"total":999996,"time":99},
{"total":999997,"time":99}
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
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result
