'''
Author: 七画一只妖
Date: 2022-03-25 18:15:05
LastEditors: 七画一只妖
LastEditTime: 2022-03-26 18:33:55
Description: file content
'''
# 和.db文件交互的模块
import os
import sqlite3

# 获取当前文件路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 建立连接data文件夹下的user_database.db数据库
conn = sqlite3.connect(f'{current_path}\\data\\user_info.db')




# 新建用户时，插入数据
def insert_user(user_id: str, user_health: int, user_armor: int, user_attack: int):
    cursor = conn.cursor()
    cursor.execute('insert into user_hp_ak_am_coin (user_id, user_health, user_armor, user_attack, user_coin) values (?, ?, ?, ?, ?)',
                   (user_id, user_health, user_armor, user_attack, 0))
    conn.commit()
    cursor.close()


# 判断用户是否存在
def is_user_exist(user_id: str):
    cursor = conn.cursor()
    cursor.execute(
        'select * from user_hp_ak_am_coin where user_id=?', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


# 根据user_id查询用户属性
def query_user_attribute(user_id: str):
    cursor = conn.cursor()
    cursor.execute(
        'select * from user_hp_ak_am_coin where user_id=?', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


# user_arms表插入数据
def insert_user_arms(user_id: str):
    cursor = conn.cursor()
    cursor.execute('insert into user_arms (user_id) values (?)',
                   (user_id,))
    conn.commit()
    cursor.close()


# 根据user_id查询user_arms表
def query_user_arms(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_arms where user_id=?', (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]


# 在user_arms表中判断user_id是否存在
def is_user_arms_exist(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_arms where user_id=?', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


# 根据user_id更新user_arms表
def update_user_arms(user_id: str, user_arms: str, arm_id: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_arms set user_arm{user_arms}_id=? where user_id=?',
                   (arm_id, user_id))
    conn.commit()
    cursor.close()


# 根据user_id武器等级置0
def update_user_arms_zero(user_id: str, user_arms: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_arms set user_arm{user_arms}_level=1 where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 根据武器位置查询武器id
def query_user_arms_id(user_id: str, user_arms: str):
    cursor = conn.cursor()
    cursor.execute(f'select user_arm{user_arms}_id from user_arms where user_id=?',
                   (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


# 根据武器位置升级武器
def update_user_arms_level(user_id: str, user_arms: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_arms set user_arm{user_arms}_level=user_arm{user_arms}_level+1 where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 根据位置查询当前武器等级
def query_user_arms_level(user_id: str, user_arms: str):
    cursor = conn.cursor()
    cursor.execute(f'select user_arm{user_arms}_level from user_arms where user_id=?',
                   (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


# 查询用户剩余金币
def query_user_coin(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select user_coin from user_hp_ak_am_coin where user_id=?',
                   (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


# 修改一定数量的金币
def update_user_coin(user_id: str, coin: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_hp_ak_am_coin set user_coin=user_coin{coin} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 修改一定数量的生命值
def update_user_health(user_id: str, health: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_hp_ak_am_coin set user_health=user_health{health} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 修改一定数量的护甲值
def update_user_armor(user_id: str, armor: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_hp_ak_am_coin set user_armor=user_armor{armor} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 修改一定数量的攻击力
def update_user_attack(user_id: str, attack: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_hp_ak_am_coin set user_attack=user_attack{attack} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


#########################################################################################
# BUFF相关


# user_buff表插入数据
def insert_user_buff(user_id: str):
    cursor = conn.cursor()
    cursor.execute('insert into user_buff (user_id,buff_1,buff_2,buff_3,buff_4,buff_5,buff_6,buff_7,buff_8) values (?,?,?,?,?,?,?,?,?)',
                   (user_id,0,0,0,0,0,0,0,0))
    conn.commit()
    cursor.close()


# 根据user_id查询user_buff表
def query_user_buff(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_buff where user_id=?', (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]
    

# 判断user_id是否存在
def is_user_buff_exist(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_buff where user_id=?', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


# 根据buff_id更新user_buff表
def update_user_buff(user_id: str, buff_id: str, buff_round: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_buff set buff_{buff_id}=buff_{buff_id}{buff_round} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 根据buff_id判断buff是否小于等于0
def is_buff_zero(user_id: str, buff_id: str):
    cursor = conn.cursor()
    cursor.execute(f'select buff_{buff_id} from user_buff where user_id=?',
                   (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result[0] <= 0:
        return True
    else:
        return False


#########################################################################################
# 技能相关


# user_skill表插入数据
def insert_user_skill(user_id: str):
    cursor = conn.cursor()
    cursor.execute('insert into user_skill (user_id,user_mp,user_str,user_int,skill_1,skill_2,skill_3,skill_4,skill_5,skill_6,skill_7,skill_8) values (?,?,?,?,?,?,?,?,?,?,?,?)',
                   (user_id,100,30,30,0,0,0,0,0,0,0,0))
    conn.commit()
    cursor.close()


# 判断user_skill表中是否存在user_id
def is_user_skill_exist(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_skill where user_id=?', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


# 根据user_id查询user_skill表
def query_user_skill(user_id: str):
    cursor = conn.cursor()
    cursor.execute('select * from user_skill where user_id=?', (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]


# 根据skill_id更新user_skill表
def update_user_skill(user_id: str, skill_id: str, skill_level: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_skill set skill_{skill_id}=skill_{skill_id}{skill_level} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()


# 根据skill_id判断skill是否小于等于0
def is_skill_zero(user_id: str, skill_id: str):
    cursor = conn.cursor()
    cursor.execute(f'select skill_{skill_id} from user_skill where user_id=?',
                   (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result[0] <= 0:
        return True
    else:
        return False


# 修改user_skill表中的user_mp
def update_user_mp(user_id: str, mp: str):
    cursor = conn.cursor()
    cursor.execute(f'update user_skill set user_mp=user_mp{mp} where user_id=?',
                   (user_id,))
    conn.commit()
    cursor.close()