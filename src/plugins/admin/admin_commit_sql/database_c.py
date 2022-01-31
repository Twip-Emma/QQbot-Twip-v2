'''
Author: 七画一只妖
Date: 2022-01-31 11:05:38
LastEditors: 七画一只妖
LastEditTime: 2022-01-31 11:32:05
Description: file content
'''
import MySQLdb
import uuid
import datetime

from tool.setting.database_setting import *


db = MySQLdb.connect(URL,USER_CARD,PASS_WORD,DATABASE, charset='utf8' )


# 执行插入、删除、修改语句
def change_sql(sql:str) -> str:
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        return f"{type(e)}"


# 执行查询语句
def select_sql(sql:str) -> bool:
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()