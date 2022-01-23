'''
Author: 七画一只妖
Date: 2022-01-22 21:42:16
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 12:29:08
Description: file content
'''
import MySQLdb
import uuid
import datetime
import random

from tool.setting.database_setting import *
from ..auto_database_connect import db


db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')


def insert_new_user(user_name, user_id, now_time) -> None:
    cursor = db.cursor()

    sql = "INSERT INTO user_info VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
        (f'{user_name}', f'{user_id}', f"{now_time}",
         f"{now_time}", "0", "0")

    cursor.execute(sql)
    db.commit()


# 老用户修改即可
def change_speak_total(user_id: str) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET speak_time_total=speak_time_total+1 WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    db.commit()


# 修改上次发言时间
def change_sign_time(user_id: str, now_time: str) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET last_speak_time='" + \
        now_time + "'WHERE user_id='" + user_id + "';"
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


# 判断用户上次发言时间时间
# 返回值：时间
def chack_user_time(user_id: str) -> str:
    cursor = db.cursor()
    sql = "SELECT last_speak_time FROM user_info WHERE user_id=" + user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    return results[0][0]


# 查出指定用户的所有信息
def find_user_info(user_id:str) -> list:
    cursor = db.cursor()
    sql = "SELECT * FROM user_info WHERE user_id=" + user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    return results[0]


# 总控
def start(user_name:str, user_id:str) -> None:
    re = chack_user(user_id=user_id)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    if re:
        user_data = find_user_info(user_id=user_id)
        if now_time != user_data[3]:
            change_sign_time(now_time=now_time,user_id=user_id)
            change_speak_total(user_id=user_id)
        else:
            change_speak_total(user_id=user_id)
    else:
        insert_new_user(user_name=user_name, user_id=user_id, now_time=now_time)