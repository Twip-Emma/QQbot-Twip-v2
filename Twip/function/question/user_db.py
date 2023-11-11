'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-18 13:00:25
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-11 15:01:36
'''

import sqlite3
import uuid
import time


# 时间间隔(秒)
CUR_TIME = 20

from pathlib import Path
ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
DB_FILE = f'{ABSOLUTE_PATH}\\time.db'

# 发送方法
def send_time(user_id) -> [bool, int]:
    # 连接到数据库
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 创建表格（如果不存在的话）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id TEXT,
            key TEXT,
            value TEXT
        )
    ''')

    # 提交更改
    conn.commit()


    # 生成随机的UUID
    random_uuid = str(uuid.uuid4())

    # 查询数据库中是否已存在该用户ID
    cursor.execute('SELECT value FROM question WHERE key = ?', (user_id,))
    result = cursor.fetchone()

    if result is None:
        # 用户ID不存在，可以发送
        cursor.execute('INSERT INTO question (id, key, value) VALUES (?, ?, ?)', (random_uuid, user_id, int(time.time())))
        conn.commit()
        conn.close()
        return [True, 0]
    else:
        # 用户ID存在，计算时间间隔
        stored_timestamp = result[0]
        current_timestamp = int(time.time())
        time_elapsed = current_timestamp - int(stored_timestamp)

        if time_elapsed > CUR_TIME:
            # 时间间隔大于10秒，可以发送
            cursor.execute('UPDATE question SET value = ? WHERE key = ?', (current_timestamp, user_id))
            conn.commit()
            conn.close()
            return [True, 0]
        else:
            # 时间间隔小于10秒，不能发送
            remaining_time = CUR_TIME - time_elapsed
            conn.close()
            return [False, remaining_time]
    