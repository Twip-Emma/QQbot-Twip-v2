'''
Author: 七画一只妖
Date: 2022-01-21 12:34:58
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 15:17:36
Description: file content
'''
import http.client
import json
import random

import jieba
import requests
# 提交测试
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from setting import Api_Key, Api_Secret, Content_Type
from tool.find_power.format_data import is_level_A

from .db import *

__plugin_meta__ = PluginMetadata(
    name='陪聊系统',
    description='从预设好的词库选择句子回答',
    usage='''@<机器人> <你想说的话>''',
    extra={'version': 'v1.0.0',
           'cost': '###0'}
)


# 常量
THIS_PATH = path.join(path.dirname(__file__))
ENVE_PATH = f"{THIS_PATH}\\erciyuan.json"


# 注册消息响应器
# 不允许向下传递，较低优先级
message_handle = on_message(rule=to_me(), block=False, priority=10)


@message_handle.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = event.user_id
    group_id = event.group_id
    message = str(event.get_message())
    # print(f"群{group_id}的{user_id}发送了一条消息：{message}")


    key_replay = '0'
    data = json.load(
        open(ENVE_PATH, 'r', encoding='utf8'))
    messageed = jieba.lcut(message)
    for mitem in messageed:
        if key_replay == '1':
            break
        if mitem in data.keys():
            msg = random.choice(data[mitem])
            await message_handle.send(msg)
            # await session.send(f'{msg}【json】')
            key_replay = '1'

    # 进入数据库词库
    if key_replay == '0':
        sql = "SELECT thekey,replay,weight FROM ckeyword WHERE thekey LIKE '%" + message + "%'"
        result = sql_dql(sql)
        a = len(result)
        if a > 0:
            klen = 0
            strg = ""
            # 我们这里匹配最长的
            for data in result:
                tlen = len(data[0])
                # 如果完全匹配
                if data[0].strip() == message:
                    priority = 95
                    strg = data[1]
                    break
                elif tlen > klen:
                    klen = tlen
                    strg = data[1]
            # content = strg + "【sqlite数据库】"
            content = strg
            await message_handle.send(content)
        else:
            conn = http.client.HTTPSConnection("i.mly.app")
            datac = json.dumps({
            "content": message,
            "type": 1,
            "from": str(user_id),
            "fromName": "你"
            })
            headers = {
            'Api-Key': Api_Key,
            'Api-Secret': Api_Secret,
            'Content-Type': Content_Type
            }

            try:
                conn.request("POST", "/reply", datac, headers)
                res = conn.getresponse()
                datac = res.read()
                datac = json.loads(datac.decode("utf-8"))
                datac = datac["data"][0]["content"]
            except:
                datac = "null"


            if datac == "null":
                target = f'	http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'
                req = requests.get(url=target)
                response_json = req.text
                talk = response_json.replace('{"result":0,"content":"',"").replace('"}',"")
                # content = talk + "【青云客api】"
                content = talk
                await message_handle.send(content)
            else:
                # content = datac + "【茉莉api】"
                content = datac
                await message_handle.send(content)
        # return IntentCommand(priority, 'keyword', args={'message': content})
    else:
        pass