import asyncio
import nonebot
# from hoshino.config import SUPERUSERS
# from hoshino import Service, priv
# from hoshino.typing import CQEvent

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent

from .sql import asql
from .api import *
from .draw import *

help = '''
arcinfo 查询b30，需等待1-2分钟
arcre   使用本地查分器查询最近一次游玩成绩【未完成】
arcre:  指令结尾带：使用est查分器查询最近一次游玩成绩【未完成】
arcre: [arcid]  使用好友码查询TA人【未完成】
arcre: [@]  使用@ 查询好友【未完成】
arcup   查询用账号添加完好友，使用该指令绑定查询账号，添加成功即可使用arcre指令【未完成】
arcbind [arcid] [arcname]   绑定用户
arcun   解除绑定
arcrd [定数] [难度] 随机一首该定数的曲目，例如：`arcrd 10.8`，`arcrd 10+`，`arcrd 9+ byd`'''

diffdict = {
    '0' : ['pst', 'past'],
    '1' : ['prs', 'present'],
    '2' : ['ftr', 'future'],
    '3' : ['byd', 'beyond']
}

# sv = Service('arcaea', manage_priv=priv.ADMIN, enable_on_default=False, visible=True, help_=help)
arcinfo = on_command('arcinfo', aliases={'arcinfo', 'ARCINFO', 'Arcinfo'})
arcbind = on_command('arcbind', aliases={'arcbind', 'ARCBIND', 'Arcbind'})
arcun = on_command('arcun', aliases={'arcun', 'Arcun', 'ARCUN'})
arcrd = on_command('arcrd', aliases={'arcrd', 'Arcrd', 'ARCRD'})
archelp = on_command('archelp')


# 获得帮助
@archelp.handle()
async def _(ev:GroupMessageEvent):
    msg = """
        arcinfo: 查你的b30（慢的一批）\n\n
        arcbind [arcid] [arcname]   绑定用户\n\n
        arcun: 解除绑定
    """
    await archelp.finish(msg)


# 查询B30
@arcinfo.handle()
async def _(ev:GroupMessageEvent):
    qqid = ev.user_id
    msg = str(ev.get_message()).strip().split()
    if ev.message[0].type == 'at':
        qqid = int(ev.message[0].data['qq'])
    result = asql.get_user(qqid)

    
    # if msg[1] != None:
    #     if msg[1].isdigit() and len(msg[1]) == 9:
    #         arcid = msg[1]
    #     else:
    #         await arcinfo.finish(message='仅可以使用好友码查询', at_sender=True)

    if not result:
        await arcinfo.finish(message='该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
    else:
        arcid = result[0]


    await arcinfo.send(message='正在查询，请耐心等待...\n速度巨慢，做好心理准备')
    info = await draw_info(arcid)
    await arcinfo.send(message=info)


# @sv.on_prefix(['arcre', 'Arcre', 'ARCRE'])
# async def _(ev:GroupMessageEvent):
#     qqid = ev.user_id
#     est = False
#     msg = ev.message.extract_plain_text().strip()
#     if ev.message[0].type == 'at':
#         qqid = int(ev.message[0].data['qq'])
#     result = asql.get_user(qqid)
#     if msg:
#         if msg.isdigit() and len(msg) == 9:
#             result = asql.get_user_code(msg)
#             if not result:
#                 await bot.finish('该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
#             user_id = result[0]
#         elif msg == ':' or msg == '：':
#             if not result:
#                 await bot.finish('该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
#             else:
#                 est = True
#                 user_id = result[0]
#         elif ':' in msg or '：' in msg:
#             user_id = msg[1:]
#             if user_id.isdigit() and len(user_id) == 9:
#                 est = True
#             else:
#                 await bot.finish('请输入正确的好友码', at_sender=True)
#         else:
#             await bot.finish('仅可以使用好友码查询', at_sender=True)
#     elif not result:
#         await bot.finish('该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
#     elif result[1] == None:
#         await bot.finish('该账号已绑定但尚未添加为好友，请联系BOT管理员添加好友并执行 arcup 指令', at_sender=True)
#     else:
#         user_id = result[1]
#     info = await draw_score(user_id, est)
#     await bot.send(info, at_sender=True)


# 随机获取一个指定定级的曲目
# @sv.on_prefix(['arcrd', 'Arcrd', 'ARCRD'])
@arcrd.handle()
async def _(ev:GroupMessageEvent):
    args: list[str] = str(ev.get_message()).strip().split()
    diff = None
    if not args[1]:
        await arcbind.finish(message='请输入定数')
    elif len(args) == 2:
        try:
            rating = float(args[1]) * 10
            if not 10 <= rating < 116:
                await arcbind.finish(message='请输入定数：1-11.5 | 9+ | 10+')
            plus = False
        except ValueError:
            if '+' in args[1] and args[1][-1] == '+':
                rating = float(args[1][:-1]) * 10
                if rating % 10 != 0:
                    await arcbind.finish(message='仅允许定数为：9+ | 10+')
                if not 90 <= rating < 110:
                    await arcbind.finish(message='仅允许定数为：9 | 10')
                plus = True
            else:
                await arcbind.finish(message='请输入定数：1-11.5 | 9+ | 10+')
    elif len(args) == 3:
        try:
            rating = float(args[1]) * 10
            plus = False
            if not 10 <= rating < 116:
                await arcbind.finish(message='请输入定数：1-11.5 | 9+ | 10+')
            if args[2].isdigit():
                if args[2] not in diffdict:
                    await arcbind.finish(message='请输入正确的难度：3 | byd | beyond')
                else:
                    diff = int(args[2])
            else:
                for d in diffdict:
                    if args[2].lower() in diffdict[d]:
                        diff = int(d)
                        break
        except ValueError:
            if '+' in args[1] and args[1][-1] == '+':
                rating = float(args[1][:-1]) * 10
                if rating % 10 != 0:
                    await arcbind.finish(message='仅允许定数为：9+ | 10+')
                if not 90 <= rating < 110:
                    await arcbind.finish(message='仅允许定数为：9 | 10')
                plus = True
                if args[2].isdigit():
                    if args[2] not in diffdict:
                        await arcbind.finish(message='请输入正确的难度：3 | byd | beyond')
                    else:
                        diff = int(args[2])
                else:
                    for d in diffdict:
                        if args[2].lower() in diffdict[d]:
                            diff = int(d)
                            break
            else:
                await arcbind.finish(message='请输入定数：1-11.5 | 9+ | 10+')
    else:
        await arcbind.finish(message='请输入正确参数')
    if not rating >= 70 and (diff == '2' or diff == '3'):
        await arcbind.finish(message='ftr | byd 难度没有定数小于7的曲目')
    msg = random_music(rating, plus, diff)
    await arcbind.send(message=msg)


# @sv.on_fullmatch(['arcup', 'arcupdate', 'Arcup'])
# async def _(ev:GroupMessageEvent):
#     if not priv.check_priv(priv.SUPERUSER):
#         await bot.finish('请联系BOT管理员更新')
#     msg = await newbind(bot)
#     await bot.send(msg, at_sender=True)


# 绑定用户
# @sv.on_prefix(['arcbind', 'ARCBIND', 'Arcbind'])
@arcbind.handle()
async def _(ev:GroupMessageEvent):
    qqid = ev.user_id
    gid = ev.group_id
    # arcid = ev.message.extract_plain_text().strip().split()
    arcid = str(ev.get_message()).strip().split()
    try:
        if not arcid[1].isdigit() and len(arcid[1]) != 9:
            await arcbind.finish(message='请重新输入好友码和用户名\n例如：arcbind 114514810 sb616', at_sender=True)
        elif not arcid[2]:
            await arcbind.finish(message='请重新输入好友码和用户名\n例如：arcbind 114514810 sb616', at_sender=True)
    except IndexError:
        await arcbind.finish(message='请重新输入好友码和用户名\n例如：arcbind 114514810 sb616', at_sender=True)
    result = asql.get_user(qqid)
    if result:
        await arcbind.finish(message='您已绑定，如需要解绑请输入arcun', at_sender=True)
    isTrue = f'请在10秒内再次确认您的账号是否正确，如不正确请输入arcun解绑\nArcid: {arcid[1]}\nArcname：{arcid[2]}'
    await arcbind.send(message=isTrue, at_sender=True)
    await asyncio.sleep(10)
    msg = bindinfo(qqid, arcid[1], arcid[2], gid)
    await arcbind.send(message=msg, at_sender=True)
    await nonebot.get_bot().send_private_msg(user_id=1157529280, message=f'Code:{arcid[1]}\nName:{arcid[2]}\n申请加为好友')


# 解除绑定
# @sv.on_fullmatch(['arcun', 'Arcun', 'ARCUN'])
@arcun.handle()
async def _(ev:GroupMessageEvent):
    qqid = ev.user_id
    result = asql.get_user(qqid)
    if result:
        if asql.delete_user(qqid):
            msg = '解绑成功'
        else:
            msg = '数据库错误'
    else:
        msg = '您未绑定，无需解绑'
    await arcun.send(message=msg, at_sender=True)