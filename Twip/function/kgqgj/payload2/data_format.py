'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-07 10:22:42
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-17 11:52:51
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import datetime
from .api import get_daily, get_date, get_daily_target, get_rate_data
from .get_image import make_image, get_rate_image, get_knife_image

# 获取日榜


async def today_report(user_id):
    data1 = await get_date()
    data2 = await get_daily()

    date_list = data1['data']['dates']  # 获取已生效的会战时间
    mamber_list = data1['data']["members"]  # 获取参战成员
    knife_today = data2["data"]["info"]  # 今天的出刀情况

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


# 获取总榜
async def all_report(user_id):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    data1 = await get_date()
    data2 = {}

    date_list = data1['data']['dates']  # 获取已生效的会战时间
    mamber_list = data1['data']["members"]  # 获取参战成员

    # 生成总报告
    report = {}
    for member in mamber_list:
        report[member["user_name"]] = {}

    for date in date_list:
        if today != date:
            data2 = await get_daily_target(date)
        else:
            data2 = await get_daily()

        knife_today = data2["data"]["info"]  # 今天的出刀情况

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


# 获取进度
async def get_rate(user_id: str):
    # 获取最新一轮是第几轮-获取当日数据round最高值
    round = 0
    data = await get_daily()
    for item in data["data"]["info"]:
        for damage in item["damage_list"]:
            if damage["round"] > round:
                round = damage["round"]

    # 接口问题，轮数大于等于25将会显示错误
    boss_damage = {}
    if round >= 25:
        # 轮数大于25的手动计算每个boss受到的伤害
        data1 = await get_date()
        date_list = data1['data']['dates']  # 获取已生效的会战时间
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        for date in date_list:
            if today != date:
                data2 = await get_daily_target(date)
            else:
                data2 = await get_daily()

            knife_today = data2["data"]["info"]  # 今天的出刀情况

            for knife in knife_today:
                for damage in knife["damage_list"]:
                    # 只计算当轮的伤害
                    if damage["round"] == round:
                        if damage["boss_name"] not in boss_damage.keys():
                            boss_damage[damage["boss_name"]] = damage["damage"]
                        else:
                            boss_damage[damage["boss_name"]
                                        ] += damage["damage"]
        # 计算剩余血量
        max_hp = 200000000
        for boss, dam in boss_damage.items():
            boss_damage[boss] = max_hp - dam

        res = await get_rate_data()
        rate = res["data"]["boss_info"]
        text = ""
        for item in rate:
            try:
                ra = boss_damage[item['boss_name']] / max_hp * 100
            except:
                ra = 100
            # 精确到2位小数
            ra = "%.2f" % ra
            try:
                text += f"轮数:{round}  {item['boss_name']}  {boss_damage[item['boss_name']]}  {ra}%   \n\n"
            except:
                text += f"轮数:{round}  {item['boss_name']}  {max_hp}  {ra}%   \n\n"
        return get_rate_image(text, user_id)
    else:
        # 轮数小于25的直接调用接口
        res = await get_rate_data()
        rate = res["data"]["boss_info"]
        text = ""
        for item in rate:
            ra = item['boss_remain_hp'] / item['boss_hp'] * 100
            # 精确到2位小数
            ra = "%.2f" % ra
            text += f"等级:{item['level']}  {item['boss_name']}  {item['boss_remain_hp']}  {ra}%   \n\n"
        return get_rate_image(text, user_id)


# 获取出刀
async def get_knife(user_id: str):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    data1 = await get_date()

    date_list = data1['data']['dates']  # 获取已生效的会战时间
    mamber_list = data1['data']["members"]  # 获取参战成员

    # 生成总报告
    report = {}
    for member in mamber_list:
        report[member["user_name"]] = {}

    for date in date_list:
        if today != date:
            data2 = await get_daily_target(date)
        else:
            data2 = await get_daily()

        # 遍历当天的数据
        knife_today = data2["data"]["info"]  # 今天的出刀情况

        for knife in knife_today:
            user_name = knife["user_name"]
            # 数据结构 日期:出刀数
            knife_count = []
            for damage in knife["damage_list"]:
                if damage["is_kill"] == 0:
                    knife_count.append(1)  # 未击杀：完整一刀，补偿刀
                else:
                    # 存在则累加damage
                    knife_count.append(0.5)  # 击杀：补偿刀，尾刀
            report[user_name][date] = calculate_attack_count(knife_count)
    return get_knife_image(data=report, user_id=user_id, date_list=date_list)


# 计算实际出刀
def calculate_attack_count(attack_list):
    total_attacks = 0  # 总攻击次数
    bonus_attacks = 0  # 赠送的攻击次数

    for attack in attack_list:
        if attack == 1:
            total_attacks += 1
        elif attack == 0.5:
            if bonus_attacks < 3:  # 每个人每天最多有三次赠送的机会
                total_attacks += 0.5
                bonus_attacks += 0.5

    if total_attacks > 3:
        total_attacks = 3

    total_attacks = int(total_attacks) if total_attacks % 1 == 0 else total_attacks

    return total_attacks


# loop = asyncio.get_event_loop()
# loop.run_until_complete(all_report())
