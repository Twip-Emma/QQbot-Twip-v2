'''
Author: 七画一只妖
Date: 2022-03-12 22:26:16
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 13:43:02
Description: file content
'''
from typing import List
import MySQLdb
import uuid
import datetime
import random
import re

from setting import *


# 分页查询
def get_message_by_time_limit(group_id:str, count:str) -> List:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    sql = """select * from message_info where group_id=%s order by time desc limit 0,%s;"""
    args = [group_id,int(count)]
    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()

    return results


# 根据用户ID查询用户昵称
def get_name_by_id(user_id:str) -> str:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    sql = """select * from user_info where user_id=%s;"""
    args = [user_id]
    cursor = db.cursor()
    cursor.execute(sql,args)
    results = cursor.fetchall()

    return results[0][0]