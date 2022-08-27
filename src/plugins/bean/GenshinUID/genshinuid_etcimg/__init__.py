'''
Author: 七画一只妖
Date: 2022-08-26 21:34:58
LastEditors: 七画一只妖
LastEditTime: 2022-08-27 09:13:18
Description: file content
'''
from pathlib import Path

from tool.find_power.format_data import is_level_S

from ..all_import import *

get_primogems_data = on_command('版本规划', aliases={'原石预估'})
get_img_data = on_regex(r'(ys查询)?(伤害乘区|血量表|抗性表)')

PRIMOGEMS_DATA_PATH = Path(__file__).parent / 'primogems_data'
IMG_PATH = Path(__file__).parent / 'img_data'
version = ['3.0', '2.8']


@get_primogems_data.handle()
@handle_exception('版本规划')
async def send_primogems_data(event:GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if not is_level_S(event):
        return
    logger.info('开始执行[图片][版本规划]')
    logger.info('[图片][版本规划]参数: {}'.format(args))
    if args:
        if str(args) in version:
            img = f'{args}.png'
        else:
            return
    else:
        img = f'{version[0]}.png'
    primogems_img = PRIMOGEMS_DATA_PATH / img
    logger.info('[图片][版本规划]访问图片: {}'.format(img))
    await matcher.finish(MessageSegment.image(primogems_img))


@get_img_data.handle()
@handle_exception('杂图')
async def send_img_data(
    event:GroupMessageEvent, matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()
):
    if not is_level_S(event):
        return
    logger.info('开始执行[图片][杂图]')
    logger.info('[图片][杂图]参数: {}'.format(args))
    img = IMG_PATH / f'{args[1]}.jpg'
    if img.exists():
        await matcher.finish(MessageSegment.image(img))
    else:
        return
