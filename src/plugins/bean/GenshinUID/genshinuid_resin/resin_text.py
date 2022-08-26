import math
from typing import List

from ..utils.mhy_api.get_mhy_data import get_daily_data
from ..utils.alias.enName_to_avatarId import enName_to_avatarId
from ..utils.alias.avatarId_and_name_covert import avatar_id_to_name

daily_im = """*数据刷新可能存在一定延迟，请以当前游戏实际数据为准
==============
原粹树脂：{}/{}{}
每日委托：{}/{} 奖励{}领取
减半已用：{}/{}
洞天宝钱：{}
参量质变仪：{}
探索派遣：
总数/完成/上限：{}/{}/{}
{}"""


def seconds2hours(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)


async def get_resin_text(uid: str) -> str:
    dailydata = await get_daily_data(uid)
    dailydata = dailydata['data']
    max_resin = dailydata['max_resin']
    rec_time = ''
    current_resin = dailydata['current_resin']
    if current_resin < 160:
        resin_recovery_time = seconds2hours(dailydata['resin_recovery_time'])
        next_resin_rec_time = seconds2hours(
            8 * 60
            - (
                (dailydata['max_resin'] - dailydata['current_resin']) * 8 * 60
                - int(dailydata['resin_recovery_time'])
            )
        )
        rec_time = f' ({next_resin_rec_time}/{resin_recovery_time})'

    current_expedition_num = dailydata['current_expedition_num']
    max_expedition_num = dailydata['max_expedition_num']
    finished_expedition_num = 0
    expedition_info: List[str] = []
    for expedition in dailydata['expeditions']:
        avatar: str = expedition['avatar_side_icon'][89:-4]
        try:
            avatar_name: str = await enName_to_avatarId(avatar)
            avatar_name: str = await avatar_id_to_name(avatar_name)
        except KeyError:
            avatar_name: str = avatar

        if expedition['status'] == 'Finished':
            expedition_info.append(f'{avatar_name} 探索完成')
            finished_expedition_num += 1
        else:
            remained_timed: str = seconds2hours(expedition['remained_time'])
            expedition_info.append(f'{avatar_name} 剩余时间{remained_timed}')

    if dailydata['transformer']['recovery_time']['reached']:
        transformer_status = '可用'
    else:
        transformer_time = dailydata['transformer']['recovery_time']
        transformer_status = '还剩{}天{}小时{}分钟可用'.format(
            transformer_time['Day'],
            transformer_time['Hour'],
            transformer_time['Minute'],
        )

    finished_task_num = dailydata['finished_task_num']
    total_task_num = dailydata['total_task_num']
    is_extra_got = '已' if dailydata['is_extra_task_reward_received'] else '未'

    resin_discount_num_limit = dailydata['resin_discount_num_limit']
    used_resin_discount_num = (
        resin_discount_num_limit - dailydata['remain_resin_discount_num']
    )

    home_coin = (
        f'{dailydata["current_home_coin"]}/{dailydata["max_home_coin"]}'
    )
    if dailydata['current_home_coin'] < dailydata['max_home_coin']:
        coin_rec_time = seconds2hours(
            int(dailydata['home_coin_recovery_time'])
        )
        coin_add_speed = math.ceil(
            (dailydata['max_home_coin'] - dailydata['current_home_coin'])
            / (int(dailydata['home_coin_recovery_time']) / 60 / 60)
        )
        home_coin += f'（{coin_rec_time} 约{coin_add_speed}/h）'

    expedition_data = '\n'.join(expedition_info)
    send_mes = daily_im.format(
        current_resin,
        max_resin,
        rec_time,
        finished_task_num,
        total_task_num,
        is_extra_got,
        used_resin_discount_num,
        resin_discount_num_limit,
        home_coin,
        transformer_status,
        current_expedition_num,
        finished_expedition_num,
        max_expedition_num,
        expedition_data,
    )
    return send_mes
