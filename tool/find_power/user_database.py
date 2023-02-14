'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-10 12:52:51
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-02-14 15:29:16
'''
import MySQLdb

from setting import URL, USER_CARD, PASS_WORD, DATABASE

# 链接
# db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')

# 查询user_info_new表指定user_id的记录
def get_user_info_new(user_id: str) -> tuple:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = f"select * from user_info_new where user_id='{user_id}'"
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data


# 向user_info_new表中插入数据
def insert_user_info_new(user_id: str) -> None:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = "insert into user_info_new(user_id,user_coin,user_health,user_crime,user_coin_max) values (%s,100,100,0,100)"
    args = (user_id,)
    cursor.execute(sql, args)
    db.commit()
    db.close()


# 扣费
# 减少user_id的user_coin字段
def reduce_user_coin(user_id: str, user_coin: int) -> None:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = f"update user_info_new set user_coin=user_coin-{user_coin} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()
    db.close()


# 修改画境币
def change_user_crime(user_id: str, num: str) -> None:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = f"update user_info_new set user_crime=user_crime{num} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()
    db.close()


# 修改行动点上限
def change_coin_max(user_id: str, num: int) -> None:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = f"update user_info_new set user_coin_max={num} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()
    db.close()