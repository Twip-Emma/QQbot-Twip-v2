'''
Author: 七画一只妖
Date: 2022-03-01 19:28:48
LastEditors: 七画一只妖
LastEditTime: 2022-03-12 19:45:56
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent


show_group_list = on_command('查看群列表')
find_user = on_command('锁定用户')


SUPER = "1157529280"


#查询机器人加入的所有群
@show_group_list.handle()
async def _(bot:Bot,session: MessageEvent):
    if str(session.user_id) != SUPER:
        await show_group_list.finish()
    try:
        group_list = await bot.get_group_list()
        msg='共有{}个群：'.format(len(group_list))
        for group in group_list:
            msg+='\n-----------------\n'+'群名:' + group['group_name'] + '\n' +'群号:' + str(group['group_id'])
        await show_group_list.send(msg)
    except Exception as e:
        await show_group_list.finish(message=f"{type(e)}")


# 在机器人加入的所有群找出这个人
@find_user.handle()
async def _(bot:Bot,session:MessageEvent):
    if str(session.user_id) != SUPER:
        await find_user.finish()

    msg = str(session.get_message()).split()

    if len(msg) == 1:
        await find_user.finish("请在指令后面输入你要搜索的用户QQ号")

    try:
        findUseId = msg[1]
        # 获取所有群的信息
        group_list = await bot.get_group_list()

        msg = '这个人在以下几个群：\n'
        for group in group_list:
            group_id = str(group['group_id'])
            group_member_list = await bot.get_group_member_list(group_id=group_id)
            for item in group_member_list:
                if str(item['user_id']) == findUseId:
                    msg +='群名：'+ group['group_name'] + '\n群号：' + str(group['group_id']) + '\n\n'
        msg += '─────────'
        await find_user.send(msg)
    except Exception as e:
        await find_user.finish(message=f"{type(e)}")