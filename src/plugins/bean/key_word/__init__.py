'''
Author: 七画一只妖
Date: 2022-01-21 12:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-04-22 23:33:10
Description: file content
'''
# 提交测试
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

import json
import jieba
import random
import http.client
import requests
import asyncio

from tool.find_power.format_data import is_level_S

from .db import *
from tool.setting.speaker_setting import Api_Key, Api_Secret, Content_Type


# 常量
THIS_PATH = path.join(path.dirname(__file__))
ENVE_PATH = f"{THIS_PATH}\\erciyuan.json"


# 注册消息响应器
message_handle = on_message(rule=to_me())


@message_handle.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        await message_handle.finish()

    await asyncio.sleep(random.randint(2, 4))

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
            await message_handle.send(message=msg, at_sender=True)
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
            await message_handle.send(message=content, at_sender=True)
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
                await message_handle.send(message=content, at_sender=True)
            else:
                # content = datac + "【茉莉api】"
                content = datac
                await message_handle.send(message=content, at_sender=True)
        # return IntentCommand(priority, 'keyword', args={'message': content})
    else:
        pass
