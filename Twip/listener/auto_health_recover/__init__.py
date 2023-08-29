'''
Author: 七画一只妖
Date: 2022-06-21 14:44:44
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 14:03:49
Description: file content
'''

import datetime

import MySQLdb
import pytz
from nonebot import require
from nonebot.plugin import PluginMetadata
from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB

__plugin_meta__ = PluginMetadata(
    name='静默者-健康回复',
    description='功能：涩图功能的健康回复系统',
    usage='''使用方式：无【静默模块】''',
    extra={'version': 'v0.0.1',
           'cost': '无消耗'}
)


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", hour="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 3 == 0:
        db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
        cursor = db.cursor()
        cursor.execute("update user_info_new set user_health=user_health+1 where user_health<100")
        db.commit()
        db.close()


@scheduler.scheduled_job("cron", hour="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    cursor.execute("update user_info_new set user_coin=IF(user_coin + 10 > user_coin_max, user_coin, user_coin + 10)")
    db.commit()
    db.close()