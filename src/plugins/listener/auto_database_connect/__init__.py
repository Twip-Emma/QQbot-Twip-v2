'''
Author: 七画一只妖
Date: 2022-01-23 10:01:59
LastEditors: 七画一只妖
LastEditTime: 2022-06-24 09:47:53
Description: file content
'''

import datetime
from nonebot import require
import pytz
import MySQLdb

# from DBUtils.PooledDB import PooledDB

from tool.setting.database_setting import *

scheduler = require("nonebot_plugin_apscheduler").scheduler
# setudb = PooledDB(MySQLdb,
#                   mincached=1,
#                   maxcached=10,
#                   maxshared=0,
#                   maxconnections=10,
#                   host=URL,
#                   user=USER_CARD,
#                   passwd=PASS_WORD,
#                   db="image_warehouse_1",
#                   port=3306,
#                   charset='utf8')


# 加载插件时就创建一次连接
db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
db2 = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')


# 每5个小时进行一次数据库连接
@scheduler.scheduled_job("cron", hour="*")
async def _():
    global db
    db.close()
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 5 == 0:
        db = MySQLdb.connect(URL, USER_CARD, PASS_WORD,
                             DATABASE, charset='utf8')


# 每5个小时进行一次数据库连接
@scheduler.scheduled_job("cron", hour="*")
async def _():
    global db2
    db2.close()
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 5 == 0:
        db2 = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')
