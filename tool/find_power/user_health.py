'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-10 12:52:51
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-11-03 21:11:20
'''
import MySQLdb

from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB

# 链接
# db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')

# 查询user_info_new表指定user_id的记录
def get_user_info_new(user_id: str) -> tuple:
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    sql = f"select * from user_info_new where user_id='{user_id}'"
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data


# 向user_info_new表中插入数据
def insert_user_info_new(user_id: str) -> None:
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    sql = "insert into user_info_new(user_id,user_health,user_health,user_crime) values (%s,100,100,0)"
    args = (user_id,)
    cursor.execute(sql, args)
    db.commit()
    db.close()


# 扣费
# 减少user_id的user_health字段
def reduce_user_health(user_id: str, user_health: int) -> None:
    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    sql = f"update user_info_new set user_health=user_health-{user_health} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()
    db.close()