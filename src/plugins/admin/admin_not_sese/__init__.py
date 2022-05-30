'''
Author: 七画一只妖
Date: 2022-05-30 14:51:59
LastEditors: 七画一只妖
LastEditTime: 2022-05-30 18:17:26
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment


from .img_format import img_format_main
from .data_format import sign_in,get_value,get_user_info


SUPER = '1157529280'


# print(img_format_main(get_value('1157529280')))
print(sign_in("1157529280"))


show_wife = on_command('看老婆')
sign_sese = on_command('自律打卡')
sese_info = on_command('自律信息')


@show_wife.handle()
async def _(bot: Bot, event: MessageEvent):
    user_id = str(event.user_id)
    if user_id == SUPER:
        await show_wife.finish(MessageSegment.image(f"file:///{img_format_main(get_value(user_id))}"))
    else:
        return


@sign_sese.handle()
async def _(bot: Bot, event: MessageEvent):
    user_id = str(event.user_id)
    if user_id == SUPER:
        await sign_sese.finish(sign_in(user_id))
    else:
        return


@sese_info.handle()
async def _(bot: Bot, event: MessageEvent):
    user_id = str(event.user_id)
    if user_id == SUPER:
        data = get_user_info(user_id)
        text = f"""
        您的自律经验值为：{data['exp']}
        您的连续自律天数为：{data['days']}
        """
        await sese_info.finish(text)
    else:
        return