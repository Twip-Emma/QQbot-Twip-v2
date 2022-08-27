'''
Author: 七画一只妖
Date: 2022-08-26 21:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-08-27 09:18:10
Description: file content
'''
from tool.find_power.format_data import is_level_S
from ..all_import import *  # noqa: F403,F401

get_help = on_command('ys帮助')

HELP_IMG = Path(__file__).parent / 'help.png'


@get_help.handle()
@handle_exception('建议')
async def send_guide_pic(event:GroupMessageEvent, matcher: Matcher):
    if not is_level_S(event):
        return
    logger.info('获得ys帮助图片成功！')
    await matcher.finish(MessageSegment.image(HELP_IMG))
