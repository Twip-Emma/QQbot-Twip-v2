'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-07 10:22:42
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-07 13:10:32
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import datetime
from .api import get_daily, get_date, get_daily_target
from .get_image import make_image

async def today_report(user_id):
    data1 = await get_date()
    data2 = await get_daily()

    date_list = data1['data']['dates'] # 获取已生效的会战时间
    mamber_list = data1['data']["members"] # 获取参战成员
    knife_today = data2["data"]["info"] # 今天的出刀情况

    # 生成今天的报告
    report = {}
    for member in mamber_list:
        report[member["user_name"]] = {}

    for knife in knife_today:
        user_name = knife["user_name"]
        # 数据结构 BOSS名称:总伤害
        for damage in knife["damage_list"]:
            # 先判断这一刀是否已经记录
            if damage["boss_name"] not in report[user_name].keys():
                # 不存在则新增
                report[user_name][damage["boss_name"]] = damage["damage"]
            else:
                # 存在则累加damage
                report[user_name][damage["boss_name"]] += damage["damage"]
    # print(report)
    return make_image(report, user_id)


async def all_report(user_id):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    data1 = await get_date()
    data2 = {}

    date_list = data1['data']['dates'] # 获取已生效的会战时间
    mamber_list = data1['data']["members"] # 获取参战成员

    # 生成总报告
    report = {}
    for member in mamber_list:
        report[member["user_name"]] = {}
    
    for date in date_list:
        if today != date:
            data2 = await get_daily_target(date)
        else:
            data2 = await get_daily()

        knife_today = data2["data"]["info"] # 今天的出刀情况

        for knife in knife_today:
            user_name = knife["user_name"]
            # 数据结构 BOSS名称:总伤害
            for damage in knife["damage_list"]:
                # 先判断这一刀是否已经记录
                if damage["boss_name"] not in report[user_name].keys():
                    # 不存在则新增
                    report[user_name][damage["boss_name"]] = damage["damage"]
                else:
                    # 存在则累加damage
                    report[user_name][damage["boss_name"]] += damage["damage"]
    # print(report)
    return make_image(report, user_id)



# loop = asyncio.get_event_loop()
# loop.run_until_complete(all_report())