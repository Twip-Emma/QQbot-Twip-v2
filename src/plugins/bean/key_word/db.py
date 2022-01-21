from os import path
import sqlite3
KEY_DB_PATH = path.join(path.dirname(__file__), 'nonebot.db')
# 数据库封装
# 把数据库的操作函数都封装到一个函数里面，避免麻烦
print(KEY_DB_PATH)
def sql_dql(sql):
    db = sqlite3.connect(KEY_DB_PATH)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
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