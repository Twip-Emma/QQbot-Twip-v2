'''
Author: 七画一只妖
Date: 2022-01-23 10:01:59
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 12:28:01
Description: file content
'''

import datetime
from nonebot import require
import nonebot
import pytz
import MySQLdb

from tool.setting.database_setting import *

scheduler = require("nonebot_plugin_apscheduler").scheduler


# 加载插件时就创建一次连接
db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')


# 每5个小时进行一次数据库连接
@scheduler.scheduled_job("cron", hour="*")
async def _():
    global db
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 5 == 0:
        db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')