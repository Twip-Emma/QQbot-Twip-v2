'''
Author: 七画一只妖
Date: 2022-02-14 12:12:53
LastEditors: 七画一只妖
LastEditTime: 2022-02-14 13:32:23
Description: file content
'''

from nonebot import on_message, on_notice
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, MessageSegment, GroupRecallNoticeEvent
from os import path
import nonebot


from PIL import Image
import base64
from io import BytesIO
import requests


# 设置要破解输出的群
DISPLAY = "274733672"

# 注册消息响应器
message_handle = on_message()

# 注册事件响应器
recall_notice = on_notice()


@message_handle.handle()
async def _(bot: Bot,event: MessageEvent, e: GroupMessageEvent):
    message = str(event.get_message())
    user_id = str(e.user_id)
    group_id = str(e.group_id)
    if "type=flash" in message:

        #获取群名
        group_list = await bot.get_group_info(group_id=group_id)
        group_name = group_list['group_name']

        recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        recall_user_name = recall_user_info['nickname']

        msg = f"在群【{group_name}({group_id})】中的{recall_user_name}({user_id})这个人发了一张闪照："

        message_list = message.split(",")
        image_url = message_list[2]
        image_url = image_url.replace("url=", "")
        resp = requests.get(image_url)
        image = Image.open(BytesIO(resp.content))
        re = img_to_b64(image)
        await bot.send_group_msg(group_id=DISPLAY, message=msg)
        await bot.send_group_msg(group_id=DISPLAY, message=MessageSegment.image(re))


@recall_notice.handle()
async def _(bot: Bot,event: MessageEvent, e: GroupMessageEvent, ree: GroupRecallNoticeEvent):
    
    if str(event.get_type) == "notice":
        print("========================")
        print(e.get_message)
        print("========================")
        #撤回消息时，获取该消息的信息
        group_id = str(ree.group_id)
        message_id = str(ree.message_id)
        user_id = str(ree.user_id)
        operator_id = str(ree.operator_id)

        #获取消息内容
        recall_msg_info = await bot.get_msg(message_id=message_id)
        recall_msg = recall_msg_info['message']

        #获取群名
        group_list = await bot.get_group_info(group_id=group_id)
        group_name = group_list['group_name']

        #获取操作双方的昵称
        recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        operator_user_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
        recall_user_name = recall_user_info['nickname']
        operator_user_name = operator_user_info['nickname']

        #消息整合
        # msg = operator_user_name + '撤回了' + recall_user_name + '的一条消息\n'
        # msg += '发生在群：' + group_name + '\n内容是：\n'
        msg = f"在群【{group_name}({group_id})】中\n{operator_user_name}({operator_id})撤回了{recall_user_name}({user_id})这个人发的一条消息："

        #发送日志
        await bot.send_group_msg(group_id=DISPLAY, message=msg)
        await bot.send_group_msg(group_id=DISPLAY, message=recall_msg)
    


# 把image对象转b64
def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
