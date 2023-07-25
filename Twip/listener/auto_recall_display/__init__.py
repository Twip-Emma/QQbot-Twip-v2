'''
Author: 七画一只妖
Date: 2022-02-14 12:12:53
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-25 09:23:51
Description: file content
'''

import base64
import re
from io import BytesIO
from nonebot import on_message, on_notice
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent,
                                         GroupRecallNoticeEvent, MessageEvent,
                                         MessageSegment)
from nonebot.plugin import PluginMetadata
from PIL import Image

__plugin_meta__ = PluginMetadata(
    name='静默者-闪照撤回',
    description='功能：破解闪照、破解撤回',
    usage='''使用方式：无【静默模块】''',
    extra={'version': 'v1.0.1',
           'cost': '无消耗'}
)


# 设置要破解输出的群
DISPLAY = "274733672"

# 注册消息响应器
message_handle = on_message(block=False, priority=1)


@message_handle.handle()
async def _(bot: Bot,event: MessageEvent, e: GroupMessageEvent):
    message = str(event.get_message())
    user_id = str(e.user_id)
    group_id = str(e.group_id)

    group_list = await bot.get_group_info(group_id=group_id)
    group_name = group_list['group_name']
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    recall_user_name = recall_user_info['nickname']

    if "type=flash" in message:
        # 发的是闪照
        image_url = from_message_get_url(message=str(event.get_message()), user_id=user_id)
        msg = f"在群【{group_name}({group_id})】中的{recall_user_name}({user_id})这个人发了一闪照：{image_url}"
        await bot.send_group_msg(group_id=DISPLAY, message=msg)
        await bot.send_group_msg(group_id=DISPLAY, message=(MessageSegment.image(image_url)))
    elif "CQ:forward" in message:
        # 发的是消息记录
        msg = f"在群【{group_name}({group_id})】中的{recall_user_name}({user_id})这个人发了一组记录："
        await bot.send_group_msg(group_id=DISPLAY, message=msg)
        await bot.send_group_msg(group_id=DISPLAY, message=message)

# 撤回消息监听
async def _recall_message(bot: Bot, grnevent: GroupRecallNoticeEvent):
    #撤回消息时，获取该消息的信息
    group_id = str(grnevent.group_id)
    message_id = str(grnevent.message_id)
    user_id = str(grnevent.user_id)
    operator_id = str(grnevent.operator_id)

    #获取消息内容
    recall_msg_info = await bot.get_msg(message_id=message_id)
    recall_msg = str(recall_msg_info['message'])

    if "<" in recall_msg or ">" in recall_msg:
        return

    #获取群名
    group_list = await bot.get_group_info(group_id=group_id)
    group_name = group_list['group_name']

    #获取操作双方的昵称
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    operator_user_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
    recall_user_name = recall_user_info['nickname']
    operator_user_name = operator_user_info['nickname']

    msg = f"在群【{group_name}({group_id})】中\n{operator_user_name}({operator_id})撤回了{recall_user_name}({user_id})这个人发的一条消息："

    # 发送日志前，需要判断消息体内是否有图片
    if "image" in recall_msg:
        image_url = from_message_get_url(message=recall_msg, user_id=user_id)
        await bot.send_group_msg(group_id=DISPLAY, message=f"{msg}{image_url}")
        await bot.send_group_msg(group_id=DISPLAY, message=MessageSegment.image(image_url))
    else:
        await bot.send_group_msg(group_id=DISPLAY, message=msg)
        await bot.send_group_msg(group_id=DISPLAY, message=recall_msg)
    

recall_message = on_notice(_recall_message)
recall_message.handle()


# 把image对象转b64
def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


# 从消息中获取图片url并返回
def from_message_get_url(message:str, user_id:str) -> str:
    comment = re.compile(r'file=(.*?).image',re.S)
    comment1 = str(comment.findall(message))
    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    x = str(re.sub(reg, '', comment1.upper()))
    image_url = ('https://gchat.qpic.cn/gchatpic_new/' + user_id + '/2640570090-2264725042-' + x.upper() + '/0?term=3')
    return image_url
