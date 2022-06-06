'''
Author: 七画一只妖
Date: 2022-06-06 18:38:36
LastEditors: 七画一只妖
LastEditTime: 2022-06-06 19:16:45
Description: file content
'''
import MySQLdb


from tool.database_handle.user_info_new import get_user_info_new,insert_user_info_new,is_exist_user_info_new
from tool.setting.database_setting import *


# 获取数据
def get_user_data_info_new(user_id:str) -> tuple:
    user_data_new = get_user_info_new(user_id=user_id)
    return user_data_new


# 查出指定用户的所有信息
def get_user_data_info_old(user_id: str) -> tuple:
    db = MySQLdb.connect(URL, USER_CARD, PASS_WORD, DATABASE, charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM user_info WHERE user_id=" + user_id
    cursor.execute(sql)
    results = cursor.fetchall()
    return results[0]


def get_data_and_format(user_id:str) -> str:
    if not is_exist_user_info_new(user_id=user_id):
        insert_user_info_new(user_id=user_id)

    data_a = get_user_data_info_new(user_id=user_id)
    data_b = get_user_data_info_old(user_id=user_id)
    message = f"""
        您的发言总数：{data_b[4]}
        金币：{data_a[1]}
        健康：{data_a[2]}
        罪恶：{data_a[3]}
    """
    return message


