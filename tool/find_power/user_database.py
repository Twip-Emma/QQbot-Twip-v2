'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-10 12:52:51
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-10 13:34:56
'''
import MySQLdb

# from setting import URL, USER_CARD, PASS_WORD, DATABASE

# 设置数据库连接
URL = "rm-8vbu4rkgv70eqp2y50o.mysql.zhangbei.rds.aliyuncs.com"

# 登录数据库的用户名
USER_CARD = "twip"

# 登录数据库的密码
PASS_WORD = f"H97$*V9@#%hiPj)ih@*98n9I!@%"

# 指定的数据库
DATABASE = "qqbot-twip-database-1"

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
    sql = "insert into user_info_new(user_id,user_coin,user_health,user_crime) values (%s,100,100,0)"
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