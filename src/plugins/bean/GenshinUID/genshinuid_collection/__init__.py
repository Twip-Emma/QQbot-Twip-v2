'''
Author: 七画一只妖
Date: 2022-08-26 21:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-08-27 09:07:06
Description: file content
'''
from ..all_import import *  # noqa: F403,F401
from .draw_collection_card import draw_collection_img
from ..utils.db_operation.db_operation import select_db
from ..utils.message.get_image_and_at import ImageAndAt
from ..utils.message.error_reply import *  # noqa: F403,F401
from ..utils.mhy_api.convert_mysid_to_uid import convert_mysid
from tool.find_power.format_data import is_level_S

get_collection_info = on_regex(
    r'^(\[CQ:at,qq=[0-9]+\])?( )?'
    r'(uid|ys查询|mys)?([0-9]+)?'
    r'(收集|宝箱|sj|bx)'
    r'(\[CQ:at,qq=[0-9]+\])?( )?$'
)


@get_collection_info.handle()
@handle_exception('查询收集信息')
async def send_collection_info(
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    matcher: Matcher,
    args: Tuple[Any, ...] = RegexGroup(),
    custom: ImageAndAt = Depends(),
):
    if not is_level_S(event):
        return
    logger.info('开始执行[查询收集信息]')
    logger.info('[查询收集信息]参数: {}'.format(args))
    at = custom.get_first_at()
    if at:
        qid = at
    else:
        qid = event.user_id

    if args[2] != 'mys':
        if args[3] is None:
            uid = await select_db(qid, mode='uid')
            uid = str(uid)
        elif len(args[3]) != 9:
            return
        else:
            uid = args[3]
    else:
        uid = await convert_mysid(args[3])
    logger.info('[查询收集信息]uid: {}'.format(uid))

    if not uid:
        await matcher.finish(UID_HINT)

    im = await draw_collection_img(uid)
    if isinstance(im, str):
        await matcher.finish(im)
    elif isinstance(im, bytes):
        await matcher.finish(MessageSegment.image(im))
    else:
        await matcher.finish('发生了未知错误,请联系管理员检查后台输出!')
