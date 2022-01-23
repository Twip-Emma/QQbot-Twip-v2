'''
Author: 七画一只妖
Date: 2021-10-04 12:01:59
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 12:34:02
Description: file content
'''

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import datetime
import json
import asyncio
import os

from nonebot import require


from tool.ascii_pro.BOX_QS import qs_box_to_lock, qs_box_unlock
from .genshin import start
bot = nonebot.get_bot()


_PATH = os.path.dirname(__file__)
FILE_PATH = f"{_PATH}\\cookie.json"
scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", hour="*")
async def _():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour == 13:
        data = json.load(open(FILE_PATH, 'r', encoding='utf8'))
        for user_id, cookie in data.items():
            try:
                cookie = qs_box_unlock(cookie)
                msg_list = start(cookie)
                logging = _to_string(msg_list)
                print("成功了")
                await bot.send_private_msg(user_id=int(user_id), message=logging)
            except:
                pass
            await asyncio.sleep(4.0)
        await bot.send_private_msg(user_id=1157529280, message="任务结束")
                


def save_userUID(user_id,uid):
    uid = qs_box_to_lock(uid)
    data = json.load(open(FILE_PATH, 'r', encoding='utf8'))
    if user_id not in data:
        new_obj = {user_id:uid}
        data.update(new_obj)
    elif user_id in data:
        data[user_id] = uid
    else:
        return KeyError

    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.close() 
        return True
    except FileExistsError or FileNotFoundError:
        return False


def _to_string(msg):
    return_msg = ""
    for item in msg:
        return_msg += f"{item}\n"
    return return_msg