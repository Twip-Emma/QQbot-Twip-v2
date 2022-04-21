'''
Author: 七画一只妖
Date: 2022-04-21 21:11:55
LastEditors: 七画一只妖
LastEditTime: 2022-04-21 21:15:13
Description: file content
'''
# 和.db文件交互的模块
import os
import MySQLdb
from tool.setting.database_setting import *

# 获取当前文件路径
current_path = os.path.dirname(os.path.abspath(__file__))


def find_user_speak(user_id:str) -> int:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        'select * from user_info where user_id=%s', (user_id,))
    results = cursor.fetchall()
    return results[0][4]