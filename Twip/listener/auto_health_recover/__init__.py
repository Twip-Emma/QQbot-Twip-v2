'''
Author: 七画一只妖
Date: 2022-06-21 14:44:44
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 13:42:23
Description: file content
'''

import datetime
from nonebot import require
import pytz
import MySQLdb


from setting import *


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", minute="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour % 3 == 0:
        db = MySQLdb.connect(URL, USER_CARD, PASS_WORD,
                             DATABASE, charset='utf8')
        cursor = db.cursor()
        cursor.execute("update user_info_new set user_health=user_health+1 where user_health<100")
        db.commit()