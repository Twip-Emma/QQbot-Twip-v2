'''
Author: 七画一只妖
Date: 2022-08-30 21:55:35
LastEditors: 七画一只妖
LastEditTime: 2022-08-30 22:08:01
Description: file content
'''
from pathlib import Path
from typing import Union

from nonebot import on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, PrivateMessageEvent

from tool.find_power.format_data import is_level_S

from ..genshinuid_meta import register_menu
from ..utils.exception.handle_exception import handle_exception

get_help = on_command('gs帮助')

HELP_IMG = Path(__file__).parent / 'help.png'


@get_help.handle()
@handle_exception('建议')
@register_menu(
    '插件帮助',
    'gs帮助',
    '查看插件功能帮助图',
    detail_des=('指令：' '<ft color=(238,120,0)>gs帮助</ft>\n' ' \n' '查看插件功能帮助图'),
)
@is_level_S
async def send_guide_pic(event: Union[GroupMessageEvent, PrivateMessageEvent], matcher: Matcher):
    logger.info('获得gs帮助图片成功！')
    await matcher.finish(MessageSegment.image(HELP_IMG))
