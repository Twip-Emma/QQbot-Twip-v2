'''
Author: 七画一只妖
Date: 2022-08-26 21:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-08-27 09:21:26
Description: file content
'''
from tool.find_power.format_data import is_level_S
from .note_text import award
from ..all_import import *  # noqa

monthly_data = on_command('每月统计', priority=priority)
# get_genshin_info = on_command('当前信息', priority=priority)


# 群聊内 每月统计 功能
@monthly_data.handle()
@handle_exception('每月统计', '获取/发送每月统计失败', '@未找到绑定信息\n' + CK_HINT)
async def send_monthly_data(
    event: MessageEvent, matcher: Matcher, args: Message = CommandArg()
):
    if not is_level_S(event):
        return
    if args:
        await monthly_data.finish()
    qid = event.sender.user_id
    uid = await select_db(qid, mode='uid')
    if not uid:
        await matcher.finish(UID_HINT)
    im = await award(uid)
    await matcher.finish(im, at_sender=True)
