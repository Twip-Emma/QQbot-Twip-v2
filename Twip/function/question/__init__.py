'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-06-04 13:13:19
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-18 13:46:03
FilePath: \QQbot-Twip-v2\Twip\function\bilibili_cover\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import httpx

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_S
from tool.QsPilUtils2.dao import text_to_image
from .main import get_question

__plugin_meta__ = PluginMetadata(
    name='计算机面试题',
    description='获取计算机岗位相关的面试题提问',
    usage='''考我''',
    extra={'version': 'v1.0.0',
           'cost': '15'}
)

question_me = on_command("考我", block=True, priority=1)


@question_me.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost=15):
    await question_me.send(MessageSegment.image(f"file:///{text_to_image(get_question(str(event.group_id)),15,(20,20))}"))