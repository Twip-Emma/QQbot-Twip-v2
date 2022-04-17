'''
Author: 七画一只妖
Date: 2022-04-09 13:49:48
LastEditors: 七画一只妖
LastEditTime: 2022-04-17 20:13:43
Description: file content
'''
import datetime
from nonebot import require
import pytz
import MySQLdb

from tool.setting.database_setting import *

scheduler = require("nonebot_plugin_apscheduler").scheduler


# 每个小时要执行的sql语句
SQL_LIST_EVERY_HOUR_1 = """update user_skill set user_mp=user_mp+7 where user_mp < 500;"""
SQL_LIST_EVERY_HOUR_2 = """update user_hp_ak_am_coin set user_health=user_health+round(user_attack*2,0) where user_health<100000;"""
SQL_LIST_EVERY_HOUR_3 = """update user_hp_ak_am_coin set user_coin=user_coin+100 where user_coin<100000;"""


# 每六个小时要执行的sql语句
SQL_LIST_EVERY_SIX_HOUR_1 = """update user_skill set user_mp=user_mp+17 where user_mp < 2000;"""
SQL_LIST_EVERY_SIX_HOUR_2 = """update user_hp_ak_am_coin set user_attack=round(user_attack * 0.95) where user_health<1;"""
SQL_LIST_EVERY_SIX_HOUR_3 = """update user_hp_ak_am_coin set user_armor=round(user_armor * 1.5) where user_health<1;"""
SQL_LIST_EVERY_SIX_HOUR_4 = """update user_hp_ak_am_coin set user_health=round(user_armor * 95) where user_health<1;"""
SQL_LIST_EVERY_SIX_HOUR_5 = """update user_hp_ak_am_coin set user_health=user_health+round(user_attack*7,0) where user_health<300000;"""
SQL_LIST_EVERY_SIX_HOUR_6 = """update user_hp_ak_am_coin set user_attack=user_attack+7;"""
SQL_LIST_EVERY_SIX_HOUR_7 = """update user_hp_ak_am_coin set user_armor=user_armor+5;"""
SQL_LIST_EVERY_SIX_HOUR_8 = """update user_hp_ak_am_coin set user_armor=round(user_armor * 1.1) where user_id='3466189618';"""


# 每5个小时进行一次数据库连接
@scheduler.scheduled_job("cron", hour="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 6 == 0:
        insert_user_skill("A")
    else:
        insert_user_skill("B")
    print("成功了")



# user_skill表插入数据
def insert_user_skill(type_p:str):
    conn = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = conn.cursor()
    if type_p == "A":
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_1)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_2)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_3)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_4)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_5)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_6)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_7)
        cursor.execute(SQL_LIST_EVERY_SIX_HOUR_8)
    elif type_p == "B":
        cursor.execute(SQL_LIST_EVERY_HOUR_1)
        cursor.execute(SQL_LIST_EVERY_HOUR_2)
        cursor.execute(SQL_LIST_EVERY_HOUR_3)
    conn.commit()
    cursor.close()