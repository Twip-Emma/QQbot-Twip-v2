'''
Author: 七画一只妖
Date: 2021-12-05 18:58:57
LastEditors: 七画一只妖
LastEditTime: 2022-01-19 19:28:11
Description: file content
'''
import MySQLdb
import uuid
import datetime
import random

from tool.setting.database_setting import *


db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')

# 新用户存入数据


def insert_new_user(user_name, user_id, now_time, coin) -> None:
    cursor = db.cursor()

    sql = "INSERT INTO user_info VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
        (f'{user_name}', f'{user_id}', f"{now_time}",
         f"{now_time}", "0", f"{coin}")

    cursor.execute(sql)
    db.commit()


# 老用户修改即可
def change_coin(user_id: str, coin: float) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET coin=coin+" + \
        str(coin) + "WHERE user_id=" + user_id
    cursor.execute(sql)
    db.commit()


# 修改时间
def change_sign_time(user_id: str, sign_time: str) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET sign_time='" + \
        sign_time + "'WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    db.commit()


# 判断用户是否存在
def chack_user(user_id: str) -> bool:
    cursor = db.cursor()
    sql = "SELECT * FROM user_info WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    if results == ():
        return False
    else:
        return True


# 判断用户签到时间
def chack_user_time(user_id: str):
    cursor = db.cursor()
    sql = "SELECT sign_time FROM user_info WHERE user_id=" + user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    return results


def sign_daily_start(user_name: str, user_id: str) -> str:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    
    coin_today = (random.randint(1000, 9999))/100
    coin_today = "%.2f" % coin_today
    re = chack_user(user_id=user_id)
    if re:  # 用户存在
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        last_sign_time = chack_user_time(user_id=user_id)
        if str(now_time) == str(last_sign_time[0][0]):
            db.close()
            return "你今天签到过了，明天再来吧~"
        else:
            change_coin(user_id=user_id, coin=coin_today)
            change_sign_time(user_id=user_id,sign_time=now_time)
            db.close()
            return "签到成功，获得" + str(coin_today) + "的货币"
    else:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        insert_new_user(user_name=user_name, user_id=user_id,
                        now_time=now_time, coin=coin_today)
        db.close()
        return "签到成功，获得" + str(coin_today) + "的货币"
