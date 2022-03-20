'''
Author: 七画一只妖
Date: 2022-03-20 14:03:39
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 16:31:32
Description: file content
'''
from ..user_config import FILE_PATH
import os


CHAR_TOTAL = f"{FILE_PATH}\\icon\\_图鉴\\"
WEP_TOTAL = f"{FILE_PATH}\\icon\\_武器\\"


# 获取CHAR_TOTAL下的所有文件名,以-分割,第一个为name,第二个为star,第三个为type,返回一个列表，每个元素为一个字典
def get_char_list():
    char_list = []
    for file in os.listdir(CHAR_TOTAL):
        file = file.replace(".png", "")
        file_name = file.split("-")
        char_list.append({"name": file_name[0], "star": file_name[1], "type": file_name[2]})
    return char_list


# 获取列表中star为5的元素
def get_high_star_list(char_list):
    high_star_list = []
    for item in char_list:
        if item["star"] == "5":
            high_star_list.append(item)
    return high_star_list


# 获取列表中star为4的元素
def get_mid_star_list(char_list):
    mid_star_list = []
    for item in char_list:
        if item["star"] == "4":
            mid_star_list.append(item)
    return mid_star_list


# 获取WEP_TOTAL下的所有文件名,以-分割,第一个为name,第二个为star,第三个为type,返回一个列表，每个元素为一个字典
def get_wep_list():
    wep_list = []
    for file in os.listdir(WEP_TOTAL):
        file = file.replace(".png", "")
        file_name = file.split("-")
        try:
            wep_list.append({"name": file_name[0], "star": file_name[1], "type": file_name[2]})
        except IndexError:
            print(file)
    return wep_list


# 获取列表中star为5的元素
def get_high_star_wep_list(wep_list):
    high_star_wep_list = []
    for item in wep_list:
        if item["star"] == "5":
            high_star_wep_list.append(item)
    return high_star_wep_list


# 获取列表中star为4的元素
def get_mid_star_wep_list(wep_list):
    mid_star_wep_list = []
    for item in wep_list:
        if item["star"] == "4":
            mid_star_wep_list.append(item)
    return mid_star_wep_list


# 获取列表中star为3的元素
def get_low_star_wep_list(wep_list):
    low_star_wep_list = []
    for item in wep_list:
        if item["star"] == "3":
            low_star_wep_list.append(item)
    return low_star_wep_list


# 角色列表
update_pool_5x = get_high_star_list(get_char_list())
update_pool_4x = get_mid_star_list(get_char_list())

# 武器列表
weap_pool_3x = get_low_star_wep_list(get_wep_list())
weap_pool_4x = get_mid_star_wep_list(get_wep_list())
weap_pool_5x = get_high_star_wep_list(get_wep_list())
