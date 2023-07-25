'''
Author: 七画一只妖
Date: 2022-01-29 14:01:06
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-25 09:08:47
Description: file content
'''
import random
import traceback
# coding=utf-8
# from hoshino import Service
# from hoshino.typing import HoshinoBot,CQEvent
from os.path import join

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State
from tool.find_power.format_data import is_level_S

from .Life import Life
from .PicClass import *

__plugin_meta__ = PluginMetadata(
    name='人生重开',
    description='这狗比人生不想呆了，重开！',
    usage='''重开|人生重开|人生重来模拟器|remake''',
    extra={'version': 'v1.0.0',
           'cost': '45'}
)


life_remake = on_command('remake', aliases={'重开',"人生重开","人生重来模拟器"})


# sv = Service("人生重来模拟器")

def genp(prop):
    ps = []
    # for _ in range(4):
    #     ps.append(min(prop, 8))
    #     prop -= ps[-1]
    tmp = prop
    while True:
        for i in range(0,4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp>=10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3]<10:
            break
        else:
            tmp = prop
            ps.clear()
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': ps[3]
    }

# @sv.on_fullmatch(("/remake","人生重来"))


@life_remake.handle()
@is_level_S
async def remake(bot:Bot, event:GroupMessageEvent, cost=45):
    pic_list = []
    mes_list = []

    Life.load(join(FILE_PATH,'data'))
    while True:
        life = Life()
        life.setErrorHandler(lambda e: traceback.print_exc())
        life.setTalentHandler(lambda ts: random.choice(ts).id)
        life.setPropertyhandler(genp)
        flag = life.choose()
        if flag:
            break

    # nonebot适配
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    name = recall_user_info['nickname']

    # name = ev["sender"]['card'] or ev["sender"]["nickname"]
    choice = 0
    person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
    for t in life.talent.talents:
        choice = choice + 1
        person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

    person = person + "\n【基础属性】\n"
    person = person + "   美貌值:" + str(life.property.CHR)+"  "
    person = person + "智力值:" + str(life.property.INT)+"  "
    person = person + "体质值:" + str(life.property.STR)+"  "
    person = person + "财富值:" + str(life.property.MNY)+"  "
    pic_list.append("这是"+name+"本次轮回的基础属性和天赋:")
    pic_list.append(ImgText(person).draw_text())

    await life_remake.send(message="你的命运正在重启....",at_sender=True)

    res = life.run() #命运之轮开始转动
    mes = '\n'.join('\n'.join(x) for x in res)
    pic_list.append("这是"+name+"本次轮回的生平:")
    pic_list.append(ImgText(mes).draw_text())

    sum = life.property.gensummary() #你的命运之轮到头了
    pic_list.append("这是" + name + "本次轮回的评价:")
    pic_list.append(ImgText(sum).draw_text())

    for img in pic_list:
        data = {
            "type": "node",
            "data": {
                "name": "Twip的替身",
                "uin": "2854196310",
                "content": img
            }
        }
        mes_list.append(data)

    await bot.send_group_forward_msg(group_id=group_id, messages=mes_list)
