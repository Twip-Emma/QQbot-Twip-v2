'''
Author: 七画一只妖
Date: 2021-11-09 20:03:46
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 14:03:21
Description: file content
'''
import MySQLdb
import uuid
import datetime

from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB


db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')


def insert_into_sql(message_id, message_context, group_id, user_id):
    cursor = db.cursor()
    uid = uuid.uuid1()
        # now_time = datetime.datetime.strptime('2021-01-21 21:48:00','%Y-%m-%d %H:%M:%S')
        # 获取当前时间
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        sql = "INSERT INTO message_info VALUES(%s, %s, %s, %s, %s, %s)"
        args = [f'{uid}', f'{message_id}', f"{message_context}",
                f"{group_id}", f"{user_id}", f"{now_time}"]
        # cursor.insert(sql, args)
        cursor.execute(sql, args)
        db.commit()
    except:
        sql = "INSERT INTO message_info VALUES(%s, %s, %s, %s, %s, %s)"
        args = [f'{uid}', f'{message_id}', '消息太长了，这是个xml卡片或者分享链接',
                f"{group_id}", f"{user_id}", f"{now_time}"]
        # cursor.insert(sql, args)
        cursor.execute(sql, args)
        db.commit()