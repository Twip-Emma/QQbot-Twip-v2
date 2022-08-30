'''
Author: 七画一只妖
Date: 2022-08-28 09:24:43
LastEditors: 七画一只妖
LastEditTime: 2022-08-28 22:21:32
Description: file content
'''
from ..all_import import *  # noqa: F403,F401

get_help = on_command('gs帮助')

HELP_IMG = Path(__file__).parent / 'help.png'


@get_help.handle()
@handle_exception('建议')
@is_level_S
async def send_guide_pic(event: Union[GroupMessageEvent, PrivateMessageEvent],matcher: Matcher):
    logger.info('获得gs帮助图片成功！')
    await matcher.finish(MessageSegment.image(HELP_IMG))
