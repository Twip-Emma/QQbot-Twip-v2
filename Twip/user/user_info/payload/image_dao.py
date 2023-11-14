'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-09-08 21:27:33
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-14 16:23:47
FilePath: \074个人信息卡片\payload\image_dao.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-09-08 21:27:33
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-09-08 21:31:07
FilePath: \074个人信息卡片\image_dao.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import random
import httpx
from PIL import Image
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]

from .image_factory import picture_paste_img, circle, write_longsh, FontEntity
from .db import sql_dml, sql_dql

from tool.find_power.user_database import get_user_info_new, insert_user_info_new, change_user_crime, change_coin_max, get_user_info_old

# 请求QQ头像
async def get_avatar(user_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://q2.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640")
        file_path = Path(BASE_PATH) / "cache" / f"avatar_{user_id[0]}.png"
        with open(file_path, "wb") as f:
            f.write(response.content)
    return str(file_path)


# 卡片合成
async def get_card(user_id: str, user_name: str) -> str:
    # 1.获取头像
    avatar_path = await get_avatar(user_id)

    # 2.背景合成
    bg_list = [x for x in Path(f"{BASE_PATH}\\image").glob("bg*.png")]
    bg_path = str(bg_list[random.randint(0, len(bg_list) - 1)])
    bg = Image.open(bg_path).convert('RGBA')
    
    card = Image.open(f"{BASE_PATH}\\image\\card.png").convert('RGBA')
    avatar = Image.open(avatar_path).convert('RGBA')
    avatar = avatar.resize((339,339))
    # 3.将avatar变成圆形

    # 4.合成
    avatar1 = circle(avatar)
    img1 = picture_paste_img(avatar1, bg, (50,772))
    img2 = picture_paste_img(card, img1)

    # 获取数据
    user_data = get_user_info_new(user_id=user_id)
    user_data_old = get_user_info_old(user_id=user_id)
    if user_data == None:
        insert_user_info_new(user_id=user_id)
        user_data = get_user_info_new(user_id=user_id)
    level_data:dict = find_coin_max(user_data[4])
    level = level_data['now_level']

    # 写字
    f_a = FontEntity()
    f_a.setSize(75).setColor("#FFFFE0")
    resp1 = write_longsh(f_a, img2, f"{level:<5}级", "C", (270, 0))

    resp2 = write_longsh(f_a.setSize(50), resp1, f"{user_name}", "C", (530, 480))

    resp2 = write_longsh(f_a, resp1, f"体力值： {user_data[1]}/{user_data[4]}", "L", (500, 660))
    resp2 = write_longsh(f_a, resp1, f"健康值： {user_data[2]}/100", "L", (500, 760))
    resp2 = write_longsh(f_a, resp1, f"画境币： {user_data[3]}", "L", (500, 860))
    resp2 = write_longsh(f_a, resp1, f"总发言： {user_data_old[4]}", "L", (500, 1060))

    rank_data = await get_speak_info(user_id=user_id)
    resp2 = write_longsh(f_a, resp1, f"总排行： {rank_data[0]}", "L", (500, 1160))
    resp2 = write_longsh(f_a, resp1, f"当日发言： {rank_data[2]}", "L", (500, 1260))
    resp2 = write_longsh(f_a, resp1, f"当日排行： {rank_data[1]}", "L", (500, 1360))

    level_txt1 = f"升级到{level_data['now_level']+1}级需要花费{level_data['level_up']}画境币\n发送 升级 即可"

    resp2 = write_longsh(f_a.setSize(35), resp1, level_txt1, "C", (1800, 1800))
    resp2 = resp2.convert("RGB")

    # 压缩图片50%
    s_path = f"""{BASE_PATH}\\cache\\resp_{user_id[0]}.jpg"""
    resp2.save(s_path, optimize=True, quality=50)
    return str(s_path)


# 获取发言排行信息
async def get_speak_info(user_id:str) -> list[str]:
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 获取用户的总榜排名
    sql = " select * from ("
    sql += " SELECT user_id, speak_time_total,"
    sql += "     RANK() OVER (ORDER BY speak_time_total DESC) AS message_rank,"
    sql += "     (SELECT COUNT(*) FROM user_info) AS total_users"
    sql += " FROM user_info ) as tt WHERE tt.user_id = '%s';"

    # 获取用户的日榜排名
    sql2 = " select user_id, speak_count, message_rank, total_users from ("
    sql2 += " SELECT user_id, speak_count, speak_time, "
    sql2 += "     RANK() OVER (ORDER BY speak_count DESC) AS message_rank,"
    sql2 += "     (SELECT COUNT(*) FROM t_bot_listener_speaklog where speak_time = '%s') AS total_users"
    sql2 += " FROM t_bot_listener_speaklog a1 WHERE a1.speak_time = '%s' ) as tt WHERE tt.user_id = '%s' and tt.speak_time = '%s';"

    data = sql_dql(sql % user_id)
    data2 = sql_dql(sql2 % (now_time, now_time, user_id, now_time))

    print(data)

    return [f"{data[0][2]} / {data[0][3]}",f"{data2[0][2]} / {data2[0][3]}",f"{data2[0][1]}"]


# 根据当前行动点上限查找下一级上限
def find_coin_max(now_max: int) -> dict:
    COIN_TABLE = {
            100:100,
            105:1000,
            110:2000,
            115:3000,
            120:4000,
            125:4500,
            130:5000,
            135:5500,
            140:6000,
            145:7000,
            150:8000,
            155:9000,
            160:10000,
            165:12500,
            170:15000,
            175:18000,
            180:22000,
            185:28000,
            190:40000,
            195:60000,
            200:100000,
            205:120000,
            210:140000,
            215:160000,
            220:180000,
            225:200000,
            230:220000,
            235:240000,
            240:260000,
            245:280000,
            250:300000,
            255:9999999
        }
    now_level = 1
    level_up = 50
    for item in COIN_TABLE.items():
        if item[0] == now_max:
            level_up = item[1]
            break
        now_level += 1

    p = now_level
    next_coin_max = None
    for item in COIN_TABLE.items():
        if p == 0:
            next_coin_max = item[0]
            break
        p -= 1

    return {
        "now_level":now_level,
        "max_level":len(COIN_TABLE),
        "level_up":level_up,
        "next_coin_max":next_coin_max
    }