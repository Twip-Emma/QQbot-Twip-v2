'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-11-12 12:26:01
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-12 12:28:16
FilePath: \079求签版本4\payload\db.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sqlite3


from pathlib import Path
ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
DB_FILE = f'{ABSOLUTE_PATH}\\sign.db'

async def sql_dql(query, params=None):
    """
    执行 SQL 查询语句

    Parameters:
        query (str): SQL 查询语句
        params (tuple, optional): 参数化查询的参数，默认为 None

    Returns:
        list: 查询结果集合
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        return result

    finally:
        conn.close()

async def sql_dml(statement, params=None):
    """
    执行 SQL 修改语句

    Parameters:
        statement (str): SQL 修改语句
        params (tuple, optional): 参数化查询的参数，默认为 None

    Returns:
        int: 受影响的行数
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(statement, params)
        else:
            cursor.execute(statement)

        conn.commit()
        return cursor.rowcount

    finally:
        conn.close()

# 示例用法：

# 查询示例
# select_query = 'SELECT * FROM user_pkg WHERE char_name = ?'
# select_params = ('John',)
# result = sql_dql(select_query, select_params)
# print(result)

# 修改示例
# update_statement = 'UPDATE user_pkg SET char_rank = ? WHERE char_name = ?'
# update_params = ('New Rank', 'John')
# affected_rows = sql_dml(update_statement, update_params)
# print(f'Affected Rows: {affected_rows}')
