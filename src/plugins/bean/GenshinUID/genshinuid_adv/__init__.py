'''
Author: 七画一只妖
Date: 2022-08-26 21:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-08-27 09:02:16
Description: file content
'''
from .get_adv import char_adv, weapon_adv
from ..all_import import *  # noqa: F401, F403
from tool.find_power.format_data import is_level_S

get_char_adv = on_regex('([\u4e00-\u9fa5]+)(用什么|能用啥|怎么养)', priority=priority)
get_weapon_adv = on_regex(
    '([\u4e00-\u9fa5]+)(能给谁|给谁用|要给谁|谁能用)', priority=priority
)


@get_char_adv.handle()
@handle_exception('建议')
async def send_char_adv(
    event:GroupMessageEvent, matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()
):
    if not is_level_S(event):
        return
    name = await alias_to_char_name(str(args[0]))
    im = await char_adv(name)
    await matcher.finish(im)


@get_weapon_adv.handle()
@handle_exception('建议')
async def send_weapon_adv(
    matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()
):
    name = await alias_to_char_name(str(args[0]))
    im = await weapon_adv(name)
    await matcher.finish(im)
