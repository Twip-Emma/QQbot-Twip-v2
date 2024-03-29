'''
Author: 七画一只妖
Date: 2022-03-01 19:28:48
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-14 13:59:40
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
import MySQLdb

from Twip import DB_URL, DB_CARD, DB_PASS, DB_LIB
from tool.QsPilUtils2.dao import text_to_image


show_group_list = on_command('查看群列表')
find_user = on_command('锁定用户')
change_user_info = on_command("修改信息")


from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name='锁定用户',
    description='在机器人所在的所有群搜索某个人',
    usage='''锁定用户 <用户QQ> | 查看群列表''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)


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
        await show_group_list.send(MessageSegment.image(f"file:///{text_to_image(msg, 15, (20, 20))}"))
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
        await find_user.send(MessageSegment.image(f"file:///{text_to_image(msg, 15, (20, 20))}"))
    except Exception as e:
        await find_user.finish(message=f"{type(e)}")


@change_user_info.handle()
async def _(bot:Bot,event: MessageEvent):
    if str(event.user_id) != SUPER:
        await find_user.finish()
    msg = str(event.get_message()).split()
    if len(msg) != 4:
        await change_user_info.finish("参数不对，需要俩参数")

    user_id = msg[1]
    add_coin = msg[2]
    add_health = msg[3]
    add_crime = msg[4]

    db = MySQLdb.connect(DB_URL, DB_CARD, DB_PASS, DB_LIB, charset='utf8')
    cursor = db.cursor()
    sql = f"update user_info_new set user_coin=user_coin{add_coin},user_health=user_health{add_health},user_crime=user_crime{add_crime} where user_id='{user_id}'"
    cursor.execute(sql)
    db.commit()
    db.close()

    await change_user_info.send("成功")