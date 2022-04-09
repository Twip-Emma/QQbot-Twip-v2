'''
Author: 七画一只妖
Date: 2022-04-09 13:49:48
LastEditors: 七画一只妖
LastEditTime: 2022-04-09 14:11:47
Description: file content
'''
import datetime
from nonebot import require
import nonebot
import pytz
import MySQLdb

from tool.setting.database_setting import *

scheduler = require("nonebot_plugin_apscheduler").scheduler


# 每个小时要执行的sql语句
SQL_LIST_EVERY_HOUR = [
    """update user_skill set user_mp=user_mp+3 where user_mp < 500;""",
    """update user_hp_ak_am_coin set user_health=user_health+335 where user_health<25000;""",
    """update user_hp_ak_am_coin set user_coin=user_coin+125 where user_coin<3500;"""
]


# 每六个小时要执行的sql语句
SQL_LIST_EVERY_SIX_HOUR = [
    """update user_skill set user_mp=user_mp+14 where user_mp < 2000;""",
    """update user_hp_ak_am_coin set user_attack=user_attack-5 where user_health<1;"""
    """update user_hp_ak_am_coin set user_armor=user_armor+20 where user_health<1;"""
    """update user_hp_ak_am_coin set user_health=5000 where user_health<1;"""
    """update user_hp_ak_am_coin set user_health=user_health+1200 where user_health<50000;""",
    """update user_hp_ak_am_coin set user_attack=user_attack+7;""",
    """update user_hp_ak_am_coin set user_armor=user_armor+3;"""
]


# 每5个小时进行一次数据库连接
@scheduler.scheduled_job("cron", hour="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 6 == 0:
        for sql in SQL_LIST_EVERY_SIX_HOUR:
            insert_user_skill(sql)
    else:
        for sql in SQL_LIST_EVERY_HOUR:
            insert_user_skill(sql)
    print("成功了")



# user_skill表插入数据
def insert_user_skill(sql:str):
    conn = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()