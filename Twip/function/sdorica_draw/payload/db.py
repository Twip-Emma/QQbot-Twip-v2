'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-11-10 21:40:41
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-11 15:57:01
FilePath: \QQbot-Twip-v2\Twip\function\sdorica_draw\payload\db.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import MySQLdb
from MySQLdb.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB

# Define your database connection pool
DB_POOL = PooledDB(
    MySQLdb,
    maxconnections=10,
    host=DB_URL,
    user=DB_CARD,
    passwd=DB_PASS,
    db=DB_LIB,
    charset='utf8',
    cursorclass=DictCursor  # Use DictCursor for dictionary-like results
)

async def create_connection():
    return DB_POOL.connection()

async def close_connection(connection):
    if connection:
        connection.close()

async def sql_dql(sql, params=None):
    connection = await create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result

    finally:
        await close_connection(connection)

async def sql_dml(sql, params=None):
    print(params)
    connection = await create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql, params)
        res = cursor.fetchone()
        connection.commit()
        return res

    except:
        connection.rollback()

    finally:
        await close_connection(connection)
