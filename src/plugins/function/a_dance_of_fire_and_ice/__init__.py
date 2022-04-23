'''
Author: 七画一只妖
Date: 2022-04-23 10:24:19
LastEditors: 七画一只妖
LastEditTime: 2022-04-23 12:54:50
Description: file content
'''
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment


from .data_format import get_song_info,add_song,del_song


MASER = "1157529280"


fi_help = on_command("冰火帮助")
fi_showall = on_command("查看冰火曲目")
fi_newsong = on_command("添加冰火曲目")
fi_deletesong = on_command("删除冰火曲目")


@fi_help.handle()
async def _(event: GroupMessageEvent):
    return await fi_help.send("""
        1.冰火帮助
        2.添加冰火曲目（参数格式：歌名 等级 出处 作者 谱师）
        3.删除冰火曲目（参数格式：歌名）
        3.查看冰火曲目
        4.记录冰火成绩（未完成）
    """)


@fi_showall.handle()
async def _(event: GroupMessageEvent):
    message_bytes = await get_song_info()
    await fi_showall.send(MessageSegment.image(f"file:///{message_bytes}"))


@fi_newsong.handle()
async def _(event: GroupMessageEvent):

    if str(event.user_id) != MASER:
        return await fi_newsong.send("你不是超级管理员，不能添加曲目")

    args = str(event.get_message()).split()
    if len(args) == 6:
        await fi_newsong.send(await add_song(args[1], args[2], args[3], args[4], args[5]))
    else:
        await fi_newsong.send("参数错误，请检查参数\n参数格式：冰火曲目 歌名 等级 出处 作者 谱师")


@fi_deletesong.handle()
async def _(event: GroupMessageEvent):
    if str(event.user_id) != MASER:
        return await fi_deletesong.send("你不是超级管理员，不能删除曲目")
    
    args = str(event.get_message()).split()
    if len(args) == 2:
        await fi_deletesong.send(await del_song(args[1]))
    else:
        await fi_deletesong.send("参数错误，请检查参数\n参数格式：冰火曲目 歌名")