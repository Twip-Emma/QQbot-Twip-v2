'''
Author: 七画一只妖
Date: 2022-01-22 21:42:16
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-09-22 19:45:30
Description: file content
'''
import MySQLdb
import datetime
import re
import uuid

from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB


db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')


def insert_new_user(user_name, user_id, now_time) -> None:
    cursor = db.cursor()

    sql = "INSERT INTO user_info VALUES(%s, %s, %s, %s, %s, %s)"
    args = [f'{user_name}', f'{user_id}',
            f"{now_time}", f"{now_time}", "0", "0"]

    cursor.execute(sql, args)
    db.commit()


# 老用户修改即可
def change_speak_total(user_id: str) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET speak_time_total=speak_time_total+1 WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    db.commit()

#############3##
# 同时修改昵称


def change_name(user_id: str, user_name: str) -> None:
    cursor = db.cursor()

    user_name = re.findall(r'[\u4e00-\u9fa5]', user_name)

    user_name = "".join(user_name)

    sql = "UPDATE user_info SET user_name=%s WHERE user_id='" + user_id + "';"
    args = [user_name]

    cursor.execute(sql, args)
    db.commit()


# 修改上次发言时间
def change_sign_time(user_id: str, now_time: str) -> None:
    cursor = db.cursor()
    sql = "UPDATE user_info SET last_speak_time='" + \
        now_time + "'WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    db.commit()


# 判断用户是否存在
def chack_user(user_id: str) -> bool:
    cursor = db.cursor()
    sql = "SELECT * FROM user_info WHERE user_id='" + user_id + "';"
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    return results


# 总控
def start(user_name: str, user_id: str) -> None:
    re = chack_user(user_id=user_id)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    if re != ():
        user_data = re[0]
        if now_time != user_data[3]:
            change_sign_time(now_time=now_time, user_id=user_id)
            change_speak_total(user_id=user_id)
        else:
            change_speak_total(user_id=user_id)
    else:
        try:
            insert_new_user(user_name=user_name,user_id=user_id, now_time=now_time)
        except:
            insert_new_user(user_name=user_id,user_id=user_id, now_time=now_time)



    # 记录每日发言 t_bot_listener_speaklog
    cursor = db.cursor()
    sql = "SELECT * FROM t_bot_listener_speaklog WHERE user_id=%s and speak_time=%s;"
    cursor.execute(sql, (user_id, now_time))
    results = cursor.fetchall()
    if results == ():
        sql = "INSERT INTO t_bot_listener_speaklog(id, user_id, user_name, speak_time, speak_count) VALUES (%s, %s, %s, %s, %s);"
        try:
            cursor.execute(sql, (uuid.uuid1(), user_id, user_name, now_time, 1))
        except:
            cursor.execute(sql, (uuid.uuid1(), user_id, get_real_name(user_name), now_time, 1))
        db.commit()
    else:
        sql = "UPDATE t_bot_listener_speaklog SET speak_count=speak_count+1 WHERE user_id=%s and speak_time=%s;"
        cursor.execute(sql, (user_id, now_time))
        db.commit()


# 获取处理后的昵称
def get_real_name(user_name:str) -> str:
    user_name = re.findall(r'[\u4e00-\u9fa5]', user_name) # 使用通配符只匹配汉字
    user_name = "".join(user_name)
    return user_name