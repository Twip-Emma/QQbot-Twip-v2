'''
Author: 七画一只妖
Date: 2022-06-18 22:21:16
LastEditors: 七画一只妖
LastEditTime: 2022-06-18 23:03:24
Description: file content
'''
import json
import os
import random
import datetime


# 获取当前路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


# 获取所有词条
def get_all_words() -> dict:
    with open(f"{BASE_PATH}\\entry.json", 'r', encoding='utf8') as f:
        data = json.load(f)
        f.close()
    return data


# 获取用户消息
def get_user_message() -> dict:
    with open(f"{BASE_PATH}\\entry_user.json", 'r', encoding='utf8') as f:
        data = json.load(f)
        f.close()
    return data


# 随机获得一个词条
def get_random_word() -> str:
    data = get_all_words()
    keys = list(data.keys())
    random_key = random.choice(keys)
    return random_key


# 添加一个词条
def add_word(word:str) -> None:
    data = get_all_words()
    new_obj = {
        len(data) :{
            "data": word,
            "level": "s"
        } 
    }
    data.update(new_obj)
    with open(f"{BASE_PATH}\\entry.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


# 取出某个用户的信息
def get_user_info(user_id:str) -> str:
    data = get_user_message()
    if user_id in data:
        return data[user_id]
    else:
        return None


# 根据id获取词条
def get_word_by_id(id:str) -> str:
    data = get_all_words()
    if id in data:
        return data[id]
    else:
        return None


# 判断是否有这个用户
def is_have_user(user_id:str) -> bool:
    data = get_user_message()
    if user_id in data:
        return True
    else:
        return False


# 新增一个用户
def add_user(user_id:str) -> None:
    data = get_user_message()
    word_id = get_random_word()

    new_user_obj = {
        user_id:{
            "time": datetime.datetime.now().strftime("%Y-%m-%d"),
            "data": word_id
        }
    }
    data.update(new_user_obj)
    with open(f"{BASE_PATH}\\entry_user.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


def update_user(user_id:str, word_id:str, time:str) -> None:
    data = get_user_message()
    data[user_id]["data"] = word_id
    data[user_id]["time"] = time
    with open(f"{BASE_PATH}\\entry_user.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()



# 主控
def function_main(user_id:str) -> str:
    if not is_have_user(user_id):
        add_user(user_id)

    user_info = get_user_info(user_id)
    if user_info["time"] == datetime.datetime.now().strftime("%Y-%m-%d"):
        _ = get_word_by_id(user_info["data"])
        message = _["data"]
        return f"""
        你今天的词条是：{message}

        你今天已经给你签过卡了，请明天再来吧
        你可以往词库里添加词条：添加涩涩词条 [词条]
        """
    else:
        word_id = get_random_word()
        update_user(user_id, word_id, datetime.datetime.now().strftime("%Y-%m-%d"))
        _ = get_word_by_id(word_id)
        message = _["data"]
        return f"""
        你今天的词条是：{message}

        新的一天！欢迎使用瑟瑟签到功能
        你可以往词库里添加词条：添加涩涩词条 [词条]
        """