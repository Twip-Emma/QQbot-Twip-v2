'''
Author: 七画一只妖
Date: 2021-11-09 20:03:46
LastEditors: 七画一只妖
LastEditTime: 2022-01-29 13:09:28
Description: file content
'''
import MySQLdb
import uuid
import datetime

from tool.setting.database_setting import *


db = MySQLdb.connect(URL,USER_CARD,PASS_WORD,DATABASE, charset='utf8' )

def insert_into_sql(message_id,message_context,group_id,user_id):
    cursor = db.cursor()

    uid = uuid.uuid1()
    # now_time = datetime.datetime.strptime('2021-01-21 21:48:00','%Y-%m-%d %H:%M:%S')
    # 获取当前时间
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')

    sql = "INSERT INTO message_info VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % \
        (f'{uid}', f'{message_id}', f"{message_context}", f"{group_id}",f"{user_id}",f"{now_time}")

    cursor.execute(sql)
    db.commit()


# def select_image(select_pid):
#     cursor = db.cursor()

#     sql = f"SELECT * FROM good_image WHERE pid='{select_pid}'"
#     try:
#         cursor.execute(sql)
#         results = cursor.fetchall()
#         for row in results:
#             pid = row[0]
#             data = row[1]
#             # 打印结果
#             return pid, data
                    
#     except:
#         print ("Error: unable to fecth data")