'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-08-30 11:27:11
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-28 15:08:21
FilePath: \QQbot-Twip-v2\Twip\speaker\key_word\db.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sqlite3
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]
KEY_DB_PATH = f"{BASE_PATH}\\nonebot.db"
# 数据库封装
# 把数据库的操作函数都封装到一个函数里面，避免麻烦
def sql_dql(sql):
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result
    except:
        return {}


def sql_dml(sql):
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        res=cursor.fetchone()
        db.commit()
        db.close()
        return res
    except:
        db.rollback()
        db.close()
        return 0