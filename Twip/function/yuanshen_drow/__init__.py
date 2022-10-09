'''
Author: 七画一只妖
Date: 2022-03-20 14:03:39
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 15:20:54
Description: file content
'''


from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from tool.find_power.format_data import is_level_S

from .database import chack_user_gacha
from .user_function import chouka_start
from .user_package import attack_chack

__plugin_meta__ = PluginMetadata(
    name='原神抽卡',
    description='模拟原神抽卡，出金概率魔改版',
    usage='''原神十连''',
    extra={'version': 'v1.0.0',
           'cost': '#150'}
)


ys_get_10 = on_command("原神十连", block=True, priority=2)


@ys_get_10.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    # 获取用户昵称
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    re = str(attack_chack(user_id))

    if re == "False":
        re = chack_user_gacha(user_id)
        await ys_get_10.finish(re)
    else:
        imgpath = await chouka_start(user_id, recall_user_name, re)
        
        await ys_get_10.send(MessageSegment.image("file:///" + imgpath))


# 参数分别是用户ID、用户昵称、剩余抽卡次数
# print(loop.run_until_complete(start("123", "456", "789")))

# 样例
# char_info = {
#                 "name": "神乐之真意",
#                 "star": "5",
#                 "type": "武器"
#             }

# print(loop.run_until_complete(init_pool_list(char_info)))
