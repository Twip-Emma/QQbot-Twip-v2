'''
Author: 七画一只妖
Date: 2022-03-25 18:07:53
LastEditors: 七画一只妖
LastEditTime: 2022-03-26 18:54:27
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, Message
from nonebot.params import CommandArg, State
from nonebot.typing import T_Handler, T_RuleChecker, T_State

# 同级
from .user_function import user_attribute,user_get_weapon,user_upgrade_weapon,user_attack,user_skill_attack,user_skill_upgrade
from tool.find_power.format_data import is_level_S


# 战斗帮助
get_help = on_command('乱斗帮助')


# 获取指令列表
@get_help.handle()
async def handle_get_help(event: GroupMessageEvent):
    if not is_level_S(event):
        await get_help.finish()
    await get_help.send(message='''
    乱斗指令列表：
    1. 乱斗帮助
    2. 我的属性
    3. 攻击/普通攻击
    4. 使用技能 (技能名称)
    5. 升级技能 (技能名称)
    6. 升级武器 (武器槽位编号)
    ''')


# 用户查看自己的属性【已完成】
# print(user_attribute("1157529280"))
my_fattribute = on_command('我的属性')


@my_fattribute.handle()
async def handle_my_fattribute(event: GroupMessageEvent):
    if not is_level_S(event):
        await my_fattribute.finish()
    image_path = user_attribute(str(event.user_id))
    await my_fattribute.send(MessageSegment.image(f"file:///{image_path}"))

# 用户获得武器
# user_get_weapon("1157529280", "10001", "1")

# 用户升级武器【已完成】
# print(user_upgrade_weapon("1157529280",1))
fupgrade_weapon = on_command('升级武器')


@fupgrade_weapon.handle()
async def handle_fupgrade_weapon(event: GroupMessageEvent):
    if not is_level_S(event):
        await fupgrade_weapon.finish()
    args = str(event.get_message()).split()
    if len(args) == 1:
        await fupgrade_weapon.send(message="请在指令后面接参数：升级的武器槽位编号")
    else:
        await fupgrade_weapon.send(message=user_upgrade_weapon(str(event.user_id), int(args[1])))
    




# 用户攻击【已完成】
# print(user_attack("1157529280","00000001"))
n_fattack = on_command('攻击')


@n_fattack.handle()
async def handle_n_fattack(event: GroupMessageEvent):
    if not is_level_S(event):
        await n_fattack.finish()

    args = str(event.get_message()).split()
    print(event.get_message())
    if len(args) == 1:
        await n_fattack.finish(message="请在指令后面接参数：目标QQ号")
    else:
        # 指令后面的参数为目标用户的QQ号
        # 指令后面的参数为被@的用户的id
        # [CQ:at,qq=1157529280]

        if "CQ:at" in str(event.get_message()):
            target_qq = str(args[1]).replace("[CQ:at,qq=","").replace("]","")
        else:
            target_qq = str(args[1])
                
        user_id = str(event.user_id)
        await n_fattack.send(message=user_attack(user_id, target_qq))
        # 判断目标用户是否存在



# 用户使用技能攻击【已完成】
# print(user_skill_attack("1157529280","00000001","攻杀剑术"))
fskill_attack = on_command('使用技能')


@fskill_attack.handle()
async def handle_fskill_attack(event: GroupMessageEvent):
    if not is_level_S(event):
        await fskill_attack.finish()
    args = str(event.get_message()).split()
    if len(args) == 1:
        await fskill_attack.finish(message="请在指令后面接参数：目标QQ号")
    else:
        # 指令后面的参数为目标用户的QQ号
        if "CQ:at" in str(event.get_message()):
            target_qq = str(args[1]).replace("[CQ:at,qq=","").replace("]","")
        else:
            target_qq = str(args[1])
        user_id = str(event.user_id)
        if len(args) == 2:
            await fskill_attack.finish(message="请在目标QQ号后面接参数：技能名称")
        else:
            skill_name = str(args[2])
            await fskill_attack.send(message=user_skill_attack(user_id, target_qq, skill_name))


# 用户升级技能
# user_skill_upgrade("1157529280","攻杀剑术")
fskill_upgrade = on_command('升级技能')


@fskill_upgrade.handle()
async def handle_fskill_upgrade(event: GroupMessageEvent):
    if not is_level_S(event):
        await fskill_upgrade.finish()
    args = str(event.get_message()).split()
    if len(args) == 1:
        await fskill_upgrade.finish(message="请在指令后面接参数：技能名称")
    else:
        skill_name = str(args[1])
        await fskill_upgrade.send(message=user_skill_upgrade(str(event.user_id), skill_name))