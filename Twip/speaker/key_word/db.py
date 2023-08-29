'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-08-30 11:27:11
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 09:26:30
FilePath: \QQbot-Twip-v2\Twip\speaker\key_word\db.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import MySQLdb

from setting import URL, USER_CARD, PASS_WORD, DATABASE
# 数据库封装
# 把数据库的操作函数都封装到一个函数里面，避免麻烦
def sql_dql(sql):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result
    except:
        return {}


def sql_dml(sql):
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
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