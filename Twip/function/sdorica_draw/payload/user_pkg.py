'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-11-10 11:40:23
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-11 16:11:37
'''
import uuid
import datetime

from .db import sql_dql, sql_dml

# 初始化背包表
async def init():
    await sql_dml('''
        CREATE TABLE IF NOT EXISTS user_pkg (
            id TEXT PRIMARY KEY,
            drow_id TEXT,
            drow_time TEXT,
            char_name TEXT,
            char_count INT,
            char_rank TEXT,
            user_id TEXT
        )
    ''')


# 查询一个用户的背包并根据char_name去重
async def get_pkg(user_id: str) -> list:
    user_pkg = await sql_dql('''
        SELECT char_name, char_rank, SUM(char_count) as total_count
        FROM user_pkg
        WHERE user_id = %s
        GROUP BY char_name, char_rank;
    ''', (user_id,))
    result = [(item['char_name'], item['char_rank'], int(item['total_count'])) for item in user_pkg]
    return sorted(result, key=lambda x: x[1], reverse=True)


# 将十连结果记录到数据库
async def add_pkg(data: list, user_id: int):
    drow_id = ''.join(str(uuid.uuid4()).split('-'))
    insert_data = []

    for item in data:
        char_count = get_char_count(item[0])
        insert_data.append((str(uuid.uuid1()),
                           drow_id,
                           datetime.datetime.now().strftime("%Y-%m-%d"),
                           item[2],
                           char_count,
                           item[0],
                           user_id))

    await add_pkg_batch(insert_data)


async def add_pkg_batch(data: list) -> bool:
    # await init() # 创建数据库

    print(str(str(tuple(data)).replace("((","(").replace("))",")")))

    await sql_dml(
        f'''
        INSERT INTO user_pkg (id, drow_id, drow_time, char_name, char_count, char_rank, user_id)
        VALUES {str(str(tuple(data)).replace("((","(").replace("))",")"))}
        ON DUPLICATE KEY UPDATE
        char_count = VALUES(char_count), drow_time = VALUES(drow_time)
        '''
    )


def get_char_count(char_rank: str) -> int:
    if char_rank == "0阶角色":
        return 1
    elif char_rank == "1阶角色":
        return 5
    elif char_rank == "2阶角色":
        return 20
    else:
        return 50