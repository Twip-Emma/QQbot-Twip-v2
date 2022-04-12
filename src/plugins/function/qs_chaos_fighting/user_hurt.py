'''
Author: 七画一只妖
Date: 2022-03-25 18:36:31
LastEditors: 七画一只妖
LastEditTime: 2022-04-11 20:49:55
Description: file content
'''
import random
from .user_buff import get_user_buff, buff_reduce
from .user_utils import *
from .user_skill import get_skill_data, get_skill_data_by_name


# 普通攻击
def normal_attack(user_id: str, target_id: str):
    user_skill_info = query_user_skill(user_id)


    # 普通攻击也有MP限制
    if user_skill_info[1] < 15:
        return False, "普通攻击消耗15MP，你的MP不足！"

    
    hp1, am1, ak1 = get_user_attribute(user_id)
    hp2, am2, ak2 = get_user_attribute(target_id)

    # 自己与目标受到了buff加成
    final_ak_up, final_am_up,_ = get_user_buff(user_id)
    print(f"宁的攻击倍率:{final_ak_up}，防御倍率:{final_am_up}")
    ak1 *= final_ak_up
    am1 *= final_am_up
    final_ak_up, final_am_up,_ = get_user_buff(target_id)
    print(f"目标的攻击倍率:{final_ak_up}，防御倍率:{final_am_up}")
    ak2 *= final_ak_up
    am2 *= final_am_up

    # 保留整数部分
    ak1 = int(ak1)
    ak2 = int(ak2)
    am1 = int(am1)
    am2 = int(am2)

    message_re = ""

    c_hit = random.randint(1, 100)
    if c_hit <= 50:
        message_re += "【暴击！】本次伤害翻倍！\n"
        ak1 *= 2


    if hp1 <= 0:
        message_re += "你已经去世了，不能再攻击了"
        return False, message_re

    if hp2 <= 0:
        message_re += "对方已经去世了，不能再攻击了"
        return False, message_re

    # 判断目标护甲值是否大于攻击者的攻击力
    if am2 >= ak1:
        message_re += "你无法击穿对方的护甲！"
        return False, message_re
    else:
        # 对方扣除生命值
        _ = ak1 - am2
        update_user_health(target_id, f"-{_}")

        # buff用一次减少一回合
        buff_reduce(user_id, target_id)

        # 技能消耗MP
        update_user_mp(user_id, f"-15")

        # 计算获得的金币
        get_coin = int(_ * 0.08)

        if hp2 - _ <= 0:
            target_coin = query_user_coin(target_id)[0]
            get_coin += int(target_coin * 0.15)
            new_tcoin = int(target_coin * 0.2)
            update_user_coin(target_id, f"-{new_tcoin}")
            update_user_coin(user_id, f"+{get_coin}")
            message_re += f"你击败了{target_id}！\n你获得了{get_coin}金币！"
            return True, message_re
        else:
            update_user_coin(user_id, f"+{get_coin}")
            message_re += f"你对{target_id}造成了{_}点伤害！，对方剩余生命值{hp2 - _}！\n你获得了{get_coin}金币！"
            return True, message_re


# 技能攻击
def skill_attack(user_id: str, target_id: str, skill_name: str):
    hp1, am1, ak1 = get_user_attribute(user_id)
    hp2, am2, ak2 = get_user_attribute(target_id)
    skill_data = get_skill_data_by_name(skill_name)
    user_skill_info = query_user_skill(user_id)
    # 判断有没有这个技能
    if skill_data == None:
        return False, "技能不存在！"

    # 先判断这个人有没有这个技能
    skill_id = skill_data['skill_id']
    if is_skill_zero(user_id, skill_id):
        return False, "你未学习这个技能！"

    # 判断用户MP是否足够
    if user_skill_info[1] < skill_data['skill_use_cost']:
        return False, "你的MP不足！"

    # 查询用户这个技能的等级
    skill_level = user_skill_info[int(skill_id) + 3]
    skill_type = skill_data['skill_type']
    user_strorint_up = 0
    if skill_type == "str":
        user_strorint_up = user_skill_info[2] # 获取用户的力量值
    elif skill_type == "int":
        user_strorint_up = user_skill_info[3] # 获取用户的智力值
    else:
        return False, "技能类型错误！"


    skill_up_total = skill_data["base_up"] + user_strorint_up # 技能总str/int值
    skill_mp_total = skill_data["base_mp"] + skill_data["mp_up"] * skill_level # 技能总倍率
    # 技能总伤害值
    skill_hurt_total = skill_up_total * skill_mp_total 

    # 技能伤害 + 自身和装备攻击力的和乘以buff倍率
    ak1 = ak1 + skill_hurt_total

    # 自己与目标受到了buff加成
    final_ak_up, final_am_up,_ = get_user_buff(user_id)
    print(f"宁的攻击倍率:{final_ak_up}，防御倍率:{final_am_up}")
    ak1 *= final_ak_up
    am1 *= final_am_up
    final_ak_up, final_am_up,_ = get_user_buff(target_id)
    print(f"目标的攻击倍率:{final_ak_up}，防御倍率:{final_am_up}")
    ak2 *= final_ak_up
    am2 *= final_am_up

    # 保留整数部分
    ak1 = int(ak1)
    ak2 = int(ak2)
    am1 = int(am1)
    am2 = int(am2)


    message_re = ""

    c_hit = random.randint(1, 100)
    if c_hit <= 50:
        message_re += "【暴击！】本次伤害翻倍！\n"
        ak1 *= 2
        
    
    if hp1 <= 0:
        message_re += "你已经去世了，不能再攻击了"
        return False, message_re

    if hp2 <= 0:
        message_re += "对方已经去世了，不能再攻击了"
        return False, message_re

    # 判断目标护甲值是否大于攻击者的攻击力
    if am2 >= ak1:
        message_re += "你无法击穿对方的护甲！"
        return False, message_re
    else:
        # 对方扣除生命值
        _ = ak1 - am2
        update_user_health(target_id, f"-{_}")

        # buff用一次减少一回合
        buff_reduce(user_id, target_id)

        # 技能消耗MP
        update_user_mp(user_id, f"-{skill_data['skill_use_cost']}")

        # 计算获得的金币
        get_coin = int(_ * 0.08)

        if hp2 - _ <= 0:
            target_coin = query_user_coin(target_id)[0]
            get_coin += int(target_coin * 0.15)
            new_tcoin = int(target_coin * 0.2)
            update_user_coin(target_id, f"-{new_tcoin}")
            update_user_coin(user_id, f"+{get_coin}")
            message_re += f"你击败了{target_id}！\n你获得了{get_coin}金币！"
            return True, message_re
        else:
            update_user_coin(user_id, f"+{get_coin}")
            message_re += f"你使用了{skill_name}对{target_id}造成了{_}点伤害！，对方剩余生命值{hp2 - _}！\n你获得了{get_coin}金币！"
            return True, message_re