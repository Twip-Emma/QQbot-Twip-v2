'''
Author: 七画一只妖
Date: 2022-01-21 12:34:58
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-28 15:07:43
Description: file content
'''
import http.client
import json
import random
from fuzzywuzzy import fuzz
import jieba
import requests
from pathlib import Path
from .db import sql_dql
# 提交测试
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from setting import Api_Key, Api_Secret
from tool.find_power.format_data import is_level_A

__plugin_meta__ = PluginMetadata(
    name='陪聊系统',
    description='从预设好的词库选择句子回答',
    usage='''使用方式：@<机器人> <你想说的话>''',
    extra={'version': 'v1.0.0',
           'cost': '5'}
)


# 常量
BASE_PATH: str = Path(__file__).absolute().parents[0]
ENVE_PATH = f"{BASE_PATH}\\erciyuan.json"

MESSAGE_JSON_DATA = json.load(open(ENVE_PATH, 'r', encoding='utf8'))


# 注册消息响应器
# 不允许向下传递，较低优先级
message_handle = on_message(rule=to_me(), block=False, priority=10)


@message_handle.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=20):
    user_id = event.user_id
    group_id = event.group_id
    message = str(event.get_message())
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']


    # 1.使用本地json文件进行匹配
    resp = get_best_response(message)
    if resp != None:
        await message_handle.send(resp)
        return

    # 2.进入数据库词库匹配
    sql = "SELECT thekey,replay,weight FROM ckeyword WHERE thekey LIKE '%" + message + "%'"
    result = sql_dql(sql)
    a = len(result)
    if a > 0:
        klen = 0
        strg = ""
        for data in result:
            tlen = len(data[0])
            if data[0].strip() == message:
                priority = 95
                strg = data[1]
                break
            elif tlen > klen:
                klen = tlen
                strg = data[1]
        content = strg
        await message_handle.send(content)
    else:
        conn = http.client.HTTPSConnection("api.mlyai.com")
        datac = json.dumps({
            "content": message,
            "type": 1,
            "from": user_id,
            "fromName": recall_user_name
        })
        headers = {
            'Api-Key': Api_Key,
            'Api-Secret': Api_Secret,
            'Content-Type': 'application/json'
        }
        try:
            # 3.尝试调用茉莉云接口
            conn.request("POST", "/reply", datac, headers)
            res = conn.getresponse()
            datac = res.read()
            datac = json.loads(datac.decode("utf-8"))
            datac = datac["data"][0]["content"]
            await message_handle.send(datac)
        except:
            # 4.调用失败改为调用青云客接口
            target = f'	http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'
            req = requests.get(url=target)
            response_json = req.text
            json_obj = json.loads(response_json)
            if json_obj["content"] == "未获取到相关信息":
                # 调用失败则返回随机信息
                await message_handle.send(random.choice(list(data)))
            else:
                await message_handle.send(content)



# 返回匹配值最高的结果
def get_best_response(message: str, fuzzy_threshold=20):
    keywords = preprocess_text(message)
    best_match = None
    highest_score = 0

    for keyword, responses in MESSAGE_JSON_DATA.items():
        score_list = []
        for user_key in keywords:
            score_list.append(fuzz.ratio(keyword, user_key))
        if max(score_list) != 0:
            print(str(max(score_list)) + "|" + keyword + "|" + str(keywords))
        if max(score_list) >= fuzzy_threshold and max(score_list) > highest_score:
            highest_score = max(score_list)
            best_match = random.choice(responses)

    return best_match


# 使用jieba分词并过滤非关键词
def preprocess_text(text):
    words = jieba.lcut(text)
    keywords = [word for word in words]
    return keywords