'''
Author: 七画一只妖
Date: 2022-04-10 09:46:03
LastEditors: 七画一只妖
LastEditTime: 2022-04-10 10:47:48
Description: file content
'''
# 获取当前文件路径
import os
import json
from .user_image import get_image, get_image_by_admin


current_path = os.path.dirname(os.path.abspath(__file__))

# 武器数据文件
arms_data_file = f"{current_path}/data/arms_data.json"


# 技能数据文件
skill_data_file = f"{current_path}/data/skill_data.json"


# 展示商店
def show_shop() -> str:
    # 获取武器数据
    with open(arms_data_file, 'r', encoding='utf-8') as f:
        arms_data:dict = json.load(f)
    # 获取技能数据
    with open(skill_data_file, 'r', encoding='utf-8') as f:
        skill_data:dict = json.load(f)

    shop_txt = ""
    shop_txt += " |   武器名称   |     花费金币      |      升级花费    |     最大等级    |      攻击力       |      防御力       |\n"
    # 遍历武器数据
    for item in arms_data:
        shop_txt += f""" {"|" + str(item["name"]).center(10) + "|"}\n\n"""
        # shop_txt += f"""{str(item["buy_cost"]):>7} | """
        # shop_txt += f"""{str(item["levle_up_cost"]).center(10) + "|"}"""
        # shop_txt += f"""{str(item["max_level"]).center(10) + "|"}"""
        # shop_txt += f"""{item["ak_start"]:>4}({"+" +str(item["ak_up"]):>4}) |"""
        # shop_txt += f"""{item["am_start"]:>4}({"+" +str(item["am_up"]):>4}) | \n"""

    shop_txt_2 = ""
    for item in arms_data:
        # shop_txt += f""" {"|" + str(item["name"]).center(10) + "|"}"""
        shop_txt_2 += f"""{str(item["buy_cost"]):>7} | """
        shop_txt_2 += f"""{str(item["levle_up_cost"]).center(10) + "|"}"""
        shop_txt_2 += f"""{str(item["max_level"]).center(10) + "|"}"""
        shop_txt_2 += f"""{item["ak_start"]:>4}({"+" +str(item["ak_up"]):>4}) |"""
        shop_txt_2 += f"""{item["am_start"]:>4}({"+" +str(item["am_up"]):>4}) | \n\n"""

    return get_image_by_admin(shop_txt,shop_txt_2)