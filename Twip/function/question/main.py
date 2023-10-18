'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-17 20:29:27
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-18 13:32:24
FilePath: \076面试题\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import random
import re
from .user_db import send_time
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]


# 加载question.json生成一个dict
def load_question():
    with open(f"{BASE_PATH}\\question.json", "r", encoding="utf-8") as f:
        return json.load(f)
    

# 获取一个问题
def get_question(key):
    check = send_time(key)
    if check[0]:
        question_dict = load_question()
        type_list = list(question_dict.keys())
        type = random.choice(type_list)
        question_list = question_dict[type]
        question = random.choice(question_list)
        # 每个句子后面都有-5，-18，-120来代表这些句子出自第多少页，现在请你去除这一部分，只保留句子
        cleaned_sentences = re.sub(r'-(\d+)$', '', question)
        resp = f"{cleaned_sentences}\n\n--{type}"
        return resp
    else:
        return f"提问冷却中，剩余时间为{check[1]}秒"