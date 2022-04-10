'''
Author: 七画一只妖
Date: 2022-04-10 09:46:03
LastEditors: 七画一只妖
LastEditTime: 2022-04-10 19:06:00
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
def show_shop_arm() -> str:
    # 获取武器数据
    with open(arms_data_file, 'r', encoding='utf-8') as f:
        arms_data:dict = json.load(f)
    # 获取技能数据
    with open(skill_data_file, 'r', encoding='utf-8') as f:
        skill_data:dict = json.load(f)

    shop_txt = "你一共有四个武器槽位，购买时发送：购买武器 [武器名字] [槽位编号]   即可购买\n"
    shop_txt += "槽位编号有1-4，每个槽位只能放置一个武器，如果槽位已经放置了武器，则覆盖\n\n\n"
    shop_txt += " |   武器名称   |     花费金币      |      升级花费    |     最大等级    |      攻击力       |      防御力       |\n\n"
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

    return get_image_by_admin(shop_txt,shop_txt_2,180)


# 展示技能
def show_shop_skill():
    # 获取技能数据
    with open(skill_data_file, 'r', encoding='utf-8') as f:
        skill_data:dict = json.load(f)

    shop_txt = "技能无需学习，你只要发送：升级技能 [技能名字]      即可升级\n"
    shop_txt += "即使你未学习这个技能，第一次使用升级也能自动学习\n\n\n"
    shop_txt += " |   技能名称   |   技能类型    |    升级花费    |   使用消耗MP值   |     最大等级    |   基础力敏增幅   |    倍率    |\n\n"
    # 遍历技能数据
    for item in skill_data:
        shop_txt += f""" {"|" + str(item["skill_name"]).center(10) + "|"}"""
        if item["skill_type"] == "str":
            shop_txt += f"""   物理伤害   |\n\n"""
        elif item["skill_type"] == "int":
            shop_txt += f"""   法术伤害   |\n\n"""
        else:
            shop_txt += f"""   虚无伤害   |\n\n"""
        
        
        # shop_txt += f"""{str(item["buy_cost"]):>7} | """
        # shop_txt += f"""{str(item["levle_up_cost"]).center(10) + "|"}"""
        # shop_txt += f"""{str(item["max_level"]).center(10) + "|"}"""
        # shop_txt += f"""{item["ak_start"]:>4}({"+" +str(item["ak_up"]):>4}) |"""
        # shop_txt += f"""{item["am_start"]:>4}({"+" +str(item["am_up"]):>4}) | \n"""

    shop_txt_2 = ""
    for item in skill_data:
        shop_txt_2 += f"""{str(item["skill_up_cost"]):>7}    | """
        shop_txt_2 += f"""{str(item["skill_use_cost"]):>7}    | """
        shop_txt_2 += f"""{str(item["skill_max_level"]):>7}    | """
        shop_txt_2 += f"""{str(item["base_up"]):>5}    | """
        shop_txt_2 += f"""{item["base_mp"]:>4}({"+" +str(item["mp_up"]):>4})    | \n\n"""
    return get_image_by_admin(shop_txt,shop_txt_2,260)