'''
Author: 七画一只妖
Date: 2022-01-29 13:26:00
LastEditors: 七画一只妖
LastEditTime: 2022-02-02 15:26:28
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from tool.find_power.format_data import is_level_S


# 注册消息响应器
common_help = on_command('common_help', aliases={'帮助', '菜单', '指令列表'})


@common_help.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        await common_help.finish()
    msg = str(event.get_message()).split()

    if len(msg) == 1:
        await common_help.finish("请重新输入该指令：\
            \n未输入第一个参数<模块>\
            \n支持的模块参数有：\
            \n功能组模块\
            \n陪聊模块\
            \n用户模块")
    elif msg[1] == "功能组模块":
        await common_help.finish("1.archelp（音游Arcaea相关功能）\
            \n2.头像表情包（制作头像表情包相关功能）\
            \n3.ph图标\
            \n4.天气<城市>（获取一个城市的天气情况）\
            \n5.重开（重启你的人生！）\
            \n5.我朋友说 <参数>")
    elif msg[1] == "陪聊模块":
        await common_help.finish("说明：艾特机器人并说出你想说的话即可获得回复\
            \n使用词库有：\
            \n1.万象群群友水群风格\
            \n2.文爱冲鼻词库\
            \n3.茉莉云词库\
            \n4.青云客词库")
    elif msg[1] == "用户模块":
        await common_help.finish("1.求签（获得一张运势卡）\
            \n2.签到（获得一定量货币）\
            \n3.个人信息（获得一张个人信息卡片）")
    else:
        await common_help.finish("没有这个模块！")



    #     try:
    #     if msg[1] == "功能组模块":
    #         await common_help.finish("1.archelp（音游Arcaea相关功能）\
    #             \n2.头像表情包（制作头像表情包相关功能）\
    #             \n3.ph图标\
    #             \n4.天气<城市>（获取一个城市的天气情况）")
    #     elif msg[1] == "陪聊模块":
    #         await common_help.finish("说明：艾特机器人并说出你想说的话即可获得回复\
    #             \n使用词库有：\
    #             \n1.万象群群友水群风格\
    #             \n2.文爱冲鼻词库\
    #             \n3.茉莉云词库\
    #             \n4.青云客词库")
    #     elif msg[1] == "用户模块":
    #         await common_help.finish("1.求签（获得一张运势卡）\
    #             \n2.签到（获得一定量货币）\
    #             \n3.个人信息（获得一张个人信息卡片）")
    #     else:
    #         await common_help.finish("没有这个模块！")
    # except:
    #     await common_help.finish("请重新输入该指令：\
    #         \n未输入第一个参数<模块>\
    #         \n支持的模块参数有：\
    #         \n功能组模块\
    #         \n陪聊模块\
    #         \n用户模块")
