'''
Author: 七画一只妖
Date: 2022-03-25 18:08:41
LastEditors: 七画一只妖
LastEditTime: 2022-03-26 23:40:54
Description: file content
'''
from email import message
import json

# 同级
from .user_database import *
from .user_utils import *
from .user_hurt import *
from .user_skill import *
from .user_image import get_image


# 用户查看自己的属性
def user_attribute(user_id:str):
        ###############################################################
    # 用户基本数据
    # 先判断用户是否存在
    if not is_user_exist(user_id):
        #新建用户
        insert_user(user_id, *generate_user_attribute())

    # 如果用户存在，则查询用户属性
    re = query_user_attribute(user_id)

    ###############################################################
    # 武器方面
    # 判断user_arms中user_id是否存在
    if not is_user_arms_exist(user_id):
        # 新建用户武器
        insert_user_arms(user_id)
    # 查询用户武器
    user_arms:list = query_user_arms(user_id)
    # 遍历user_arms，每两项为一组，分别为武器id和武器等级，生成一个字典
    user_arms_dict = []
    user_arms_dict_index = 0
    for i in range(0, len(user_arms)):
        if i == 0:
            continue
        if user_arms_dict_index % 2 == 0:
            # 列表添加一个元素
            user_arms_dict.append({user_arms[user_arms_dict_index+1]: user_arms[user_arms_dict_index + 2]})
        user_arms_dict_index += 1    
    # 遍历user_arms_dict，key是武器id，value是武器等级
    # 将key传给get_weapon_data()，获取武器数据
    ex_hp = 0
    ex_ak = 0
    ex_am = 0
    for item in user_arms_dict:
        (key, value), = item.items()
        if key == None or value == None:
            continue
        _ = get_weapon_data(key)
        ex_hp += _['hp_start'] + value * _['hp_up']
        ex_ak += _['ak_start'] + value * _['ak_up']
        ex_am += _['am_start'] + value * _['am_up']

    message_re = ""
    # 输出用户属性，算上ex_hp, ex_ak, ex_am
    message_re += f"用户ID：{user_id}\n===========================\n"
    message_re += f"用户属性：基础值+装备加成\n"
    message_re += f"用户生命值：{re[1]} + {ex_hp} = {re[1] + ex_hp}\n"
    message_re += f"用户护甲值：{re[2]} + {ex_am} = {re[2] + ex_am}\n"
    message_re += f"用户攻击力：{re[3]} + {ex_ak} = {re[3] + ex_ak}\n\n===========================\n"

    # 获取用户当前BUFF
    _, _, buff_list = get_user_buff(user_id)
    message_re += f"用户BUFF：\n"
    buff_index = 1
    for item in buff_list:
        (key, value), = item.items()
        message_re += f"【{key} x{value}】"
        # 每4个BUFF换行
        if buff_index % 4 == 0:
            message_re += "\n"
        buff_index += 1

    # 获取用户拥有的装备
    # 查询用户武器
    message_re += f"\n===========================\n用户装备：\n"
    # message_re += f"""{_["name"]}(Lv:{value})|装备加成：+{ex_hp_total:>5}|+{ex_ak_total:>5}|+{ex_am_total:>5}\n"""
    user_arms:list = query_user_arms(user_id)
    for item in user_arms_dict:
        (key, value), = item.items()
        if key == None or value == None:
            continue
        if value == 0:
            continue
        _ = get_weapon_data(key)
        ex_hp_total = _['hp_start'] + value * _['hp_up']
        ex_ak_total = _['ak_start'] + value * _['ak_up']
        ex_am_total = _['am_start'] + value * _['am_up']
        # message_re += f"""{_["name"]}(Lv:{value})|装备加成：+{ex_hp_total}/+{ex_ak_total}/+{ex_am_total}\n"""
        # 对齐
        message_re += f"""{_["name"]}(Lv:{value})|装备加成：+{ex_hp_total:>5}|+{ex_ak_total:>5}|+{ex_am_total:>5}\n"""
    
    # 查询用户技能
    if not is_user_skill_exist(user_id):
        # 新建用户技能
        insert_user_skill(user_id)
    message_re += f"\n===========================\n用户技能：\n"
    user_skill:list = query_user_skill(user_id)
    message_re += f"力量与智力：{user_skill[2]} | {user_skill[3]} （物理加成|法术加成）\n"
    message_re += f"剩余MP值： {user_skill[1]} （上限1000，恢复35/小时）\n"
    for i in range(1,9):
        if user_skill[i+3] <= 0:
            continue
        _ = get_skill_data(str(i))
        skill_type = ""
        if _["skill_type"] == "str":
            skill_type = "物理伤害"
        elif _["skill_type"] == "int":
            skill_type = "法术伤害"
        else:
            return "技能类型错误"

        skill_mp_total = _["base_mp"] + user_skill[i+3] * _["mp_up"]

        # message_re += f"""【{skill_type}】{_["skill_name"]}(Lv:{user_skill[i+3]})|当前倍率：{skill_mp_total}\n"""
        # 对齐
        message_re += f"""【{skill_type}】{_["skill_name"]}(Lv:{user_skill[i+3]:>2})|当前倍率：{skill_mp_total:>3}\n"""

    
    # 生成图片获得图片路径
    re_image = get_image(message_re,user_id=user_id)
    # re_image.show()

    return re_image


# 用户获得武器
def user_get_weapon(user_id:str, weapon_name:str, weapon_pos:int):
    # 获取这个武器的id
    _ = get_weapon_data_by_name(weapon_name)
    if _ == None:
        return "武器不存在"
    weapon_id = _["id"]


    # 判断user_arms中user_id是否存在
    if not is_user_arms_exist(user_id):
        # 新建用户武器
        insert_user_arms(user_id)

    # 判断用户是否拥有这个武器
    _ = query_user_arms_level(user_id, weapon_pos)[0]
    arm_id = query_user_arms_id(user_id, weapon_pos)[0]
    if _ and _ > 0 and arm_id == weapon_id:
        return "用户已经拥有该武器"


    # 获取升级武器的开销
    buy_cost = get_weapon_data(weapon_id)["buy_cost"]
    user_coin_now = query_user_coin(user_id)[0]
    # 判断用户是否拥有足够的金币
    if user_coin_now < buy_cost:
        return f"""购买需要{get_weapon_data(weapon_id)["buy_cost"]}金币\n宁金币不足"""
        

    update_user_arms(user_id, weapon_pos, weapon_id)
    update_user_arms_zero(user_id, weapon_pos)
    update_user_coin(user_id, f"-{buy_cost}")

    # 获取武器详细信息
    weapon_data = get_weapon_data(weapon_id)
    # 打印武器信息
    return "购买成功！"


# 用户给某个武器升级
def user_upgrade_weapon(user_id:str, weapon_pos:int):
    # weapon_pos只能是1-2
    if weapon_pos not in [1,2]:
        return "你没有这个装备槽位"

    # 判断user_arms中user_id是否存在
    if not is_user_arms_exist(user_id):
        # 新建用户武器
        insert_user_arms(user_id)

    # 获取这个位置的武器ID，然后查询武器详细信息
    arm_id = query_user_arms_id(user_id, weapon_pos)[0]
    if arm_id == None:
        return "该装备槽位没有装备"

    # 获取升级武器的开销
    levle_up_cost = get_weapon_data(arm_id)["levle_up_cost"]
    user_coin_now = query_user_coin(user_id)[0]
    # 判断用户是否拥有足够的金币
    if user_coin_now < levle_up_cost:
        return "金币不足"

    # 获取这个位置的武器ID，然后查询武器详细信息
    # arm_id = query_user_arms_id(user_id, weapon_pos)[0]
    now_level = query_user_arms_level(user_id, weapon_pos)[0]
    max_level = get_weapon_data(arm_id)["max_level"]
    if now_level <= 0:
        return "当前位置没有装备"

    if now_level >= max_level:
        return "该装备已经满级"
    
    # 升级武器
    update_user_coin(user_id, f"-{levle_up_cost}")
    update_user_arms_level(user_id, weapon_pos)
    return "升级成功！"


# 用户攻击另一个用户
def user_attack(user_id:str, target_id:str):
    # 两个参数不能相等
    if user_id == target_id:
        print("不能攻击自己")
        return

    _, message = normal_attack(user_id, target_id)
    return message


# 用户使用技能攻击另一个用户
def user_skill_attack(user_id:str, target_id:str, skill_name:str):
    # 两个参数不能相等
    if user_id == target_id:
        print("不能攻击自己")
        return

    # 新建技能信息
    if not is_user_skill_exist(user_id):
        insert_user_skill(user_id)

    # 进行攻击
    _,message = skill_attack(user_id, target_id, skill_name)
    return message


# 用户升级技能
def user_skill_upgrade(user_id:str, skill_name:str):
    # 新建技能信息
    if not is_user_skill_exist(user_id):
        insert_user_skill(user_id)

    skill_data = get_skill_data_by_name(skill_name)
    if skill_data == None:
        return "没有这个技能"


    user_skill_info = query_user_skill(user_id)
    skill_id = skill_data["skill_id"]
    skill_max_level = skill_data["skill_max_level"]
    skill_now_level = user_skill_info[int(skill_id) + 3]

    # 判断技能是否存在
    if is_skill_zero(user_id, skill_id):
        return "你没有学会这个技能！"


    # 判断技能是否满级
    if skill_now_level >= skill_max_level:
        return "技能已经满级"

    # 判断金币是否足够
    skill_upgrade_cost = skill_data["skill_up_cost"]
    user_coin_now = query_user_coin(user_id)[0]
    if user_coin_now < skill_upgrade_cost:
        return "金币不足"

    # 升级技能
    update_user_skill(user_id, skill_id, f"+1")
    update_user_coin(user_id, f"-{skill_upgrade_cost}") # 扣除金币
    return f"升级成功\n{skill_name}升到了{skill_now_level + 1}级"