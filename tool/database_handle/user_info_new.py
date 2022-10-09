'''
Author: 七画一只妖
Date: 2022-06-05 19:24:10
LastEditors: 七画一只妖
LastEditTime: 2022-06-05 20:12:02
Description: file content
'''
import MySQLdb


from tool.setting.database_setting import URL, USER_CARD, PASS_WORD, DATABASE


db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')


# 查询user_info_new表指定user_id的记录
def get_user_info_new(user_id: str) -> tuple:
    cursor = db.cursor()
    sql = f"select * from user_info_new where user_id='{user_id}'"
    cursor.execute(sql)
    data = cursor.fetchone()
    return data


# 判断user_info_new表中是否存在指定user_id的记录
def is_exist_user_info_new(user_id: str) -> bool:
    cursor = db.cursor()
    sql = f"select * from user_info_new where user_id='{user_id}'"
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False


# 向user_info_new表中插入数据
def insert_user_info_new(user_id: str) -> None:
    cursor = db.cursor()
    sql = "insert into user_info_new(user_id,user_coin,user_health,user_crime) values (%s,0,100,0)"
    args = (user_id,)
    cursor.execute(sql, args)
    db.commit()


# 查询user_id的user_health字段
def get_user_health(user_id: str) -> int:
    cursor = db.cursor()
    sql = f"select user_health from user_info_new where user_id='{user_id}'"
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    return data


# 减少user_id的user_health字段
def reduce_user_health(user_id: str, user_health: int) -> None:
    cursor = db.cursor()
    sql = f"update user_info_new set user_health=user_health-{user_health} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()