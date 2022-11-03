'''
Author: 七画一只妖
Date: 2022-05-30 21:24:00
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-11-03 20:47:03
Description: file content
'''
import MySQLdb


from setting import URL, USER_CARD, PASS_WORD, DATABASE

# db = setudb.connection()

# db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')


# 查询指定表中的数据个数
def get_count(table_name):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')
    cursor = db.cursor()
    sql = f"select count(*) from {table_name}"
    cursor.execute(sql)
    count = cursor.fetchone()[0]
    db.close()
    return count


# 向指定表中插入数据：image_id,content,real_name
def insert_data(table_name, image_id, content, real_name):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')
    cursor = db.cursor()
    sql = "insert into " + table_name + "(image_id,content,real_name) values (%s,%s,%s)"
    args = (image_id, content, real_name)
    cursor.execute(sql, args)
    db.commit()
    db.close()


# 查询第n个数据
def get_data(table_name, n):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')
    cursor = db.cursor()
    sql = f"select * from {table_name} limit {n},1"
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    return data


# 判断real_name字段的值是否存在
def is_exist(table_name, real_name):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, "image_warehouse_1", charset='utf8')
    cursor = db.cursor()
    sql = f"select * from {table_name} where real_name='{real_name}'"
    cursor.execute(sql)
    data = cursor.fetchone()
    db.close()
    if data:
        return True
    else:
        return False


# 获取用户发言数
def find_user_speak(user_id:str) -> int:
    db2 = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db2.cursor()
    cursor.execute(
        'select * from user_info where user_id=%s', (user_id,))
    results = cursor.fetchall()
    db2.close()
    return results[0][4]