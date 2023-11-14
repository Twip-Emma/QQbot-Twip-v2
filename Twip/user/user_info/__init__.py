'''
Author: 七画一只妖
Date: 2022-01-18 21:03:02
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-14 16:21:02
Description: file content
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from tool.find_power.format_data import is_level_S
from tool.utils.logger import logger as my_logger
from tool.QsPilUtils2.dao import text_to_image
from tool.find_power.user_database import get_user_info_new, insert_user_info_new, change_user_crime, change_coin_max

from .payload.image_dao import get_card


__plugin_meta__ = PluginMetadata(
    name='个人信息',
    description='查看自己的行动点和健康值',
    usage='''使用方式：个人信息''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)


get_luck = on_command("个人信息", block=True, priority=2)


# 个人信息
@get_luck.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    group_id = str(event.group_id)
    user_id = str(event.user_id)

    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    await get_luck.send(MessageSegment.image(f"file:///{await get_card(user_id=user_id, user_name=recall_user_name)}"))

    my_logger.success(
        '个人信息查询', f'成功发送：用户：<m>{recall_user_name}{user_id}</m> | 群：<m>{group_id}</m>')


# 升级
h_level_up = on_command("升级", block=True, priority=2)

@h_level_up.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    group_id = str(event.group_id)
    user_id = str(event.user_id)

    user_data = get_user_info_new(user_id=user_id)
    if user_data == None:
        insert_user_info_new(user_id=user_id)
        user_data = get_user_info_new(user_id=user_id)
    level_data:dict = find_coin_max(user_data[4])

    # 判断画境币是否足够
    if level_data["level_up"] > user_data[3]:
        await h_level_up.send(message=f"画境币不足，需要{level_data['level_up']}而你只有{user_data[3]}\n通过发言即可获得画境币", at_sender=True)
        return
    else:
        change_user_crime(user_id=user_id, num=f"-{level_data['level_up']}")
        change_coin_max(user_id=user_id, num=level_data['next_coin_max'])
        await h_level_up.send(message=f"升级！\n行动点上限增加到：{level_data['next_coin_max']}\n画境币减少：{level_data['level_up']}", at_sender=True)





# 根据当前行动点上限查找下一级上限
def find_coin_max(now_max: int) -> dict:
    COIN_TABLE = {
            100:100,
            105:1000,
            110:2000,
            115:3000,
            120:4000,
            125:4500,
            130:5000,
            135:5500,
            140:6000,
            145:7000,
            150:8000,
            155:9000,
            160:10000,
            165:12500,
            170:15000,
            175:18000,
            180:22000,
            185:28000,
            190:40000,
            195:60000,
            200:100000,
            205:120000,
            210:140000,
            215:160000,
            220:180000,
            225:200000,
            230:220000,
            235:240000,
            240:260000,
            245:280000,
            250:300000,
            255:9999999
        }
    now_level = 1
    level_up = 50
    for item in COIN_TABLE.items():
        if item[0] == now_max:
            level_up = item[1]
            break
        now_level += 1

    p = now_level
    next_coin_max = None
    for item in COIN_TABLE.items():
        if p == 0:
            next_coin_max = item[0]
            break
        p -= 1

    return {
        "now_level":now_level,
        "max_level":len(COIN_TABLE),
        "level_up":level_up,
        "next_coin_max":next_coin_max
    }