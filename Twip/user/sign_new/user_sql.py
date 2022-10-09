'''
Author: 七画一只妖
Date: 2021-12-05 18:58:57
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 13:56:41
Description: file content
'''
import datetime

from os import path
import sqlite3

from Twip import ABSOLUTE_PATH
FILE_PATH = f"{ABSOLUTE_PATH}\\user\\sign_new"
KEY_DB_PATH = path.join(FILE_PATH, 'user_sign_info.db')

# 新用户存入数据
def insert_new_user(user_id:str, info:str) -> None:
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()

    sql = "insert into user_sign_info (user_id, sign_time, info)values('" \
        + user_id + "','" + now_time + "','" + info + "');"

    cursor.execute(sql)
    db.commit()
    db.close()
    

# 修改时间和签到内容
def change_sign_info(user_id: str, info: str) -> None:
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()
    sql = "UPDATE user_sign_info SET sign_time='" + \
        now_time + "' , info='" + info + "'WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    db.commit()
    db.close()


# 根据ID查询用户
def select_user(user_id: str) -> tuple:
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()
    sql = "SELECT * FROM user_sign_info WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results
