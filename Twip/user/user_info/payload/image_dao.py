'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-09-08 21:27:33
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-09-09 14:27:25
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
import random
import httpx
from PIL import Image
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]

from .image_factory import picture_paste_img, circle, write_longsh, FontEntity

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

    resp2 = write_longsh(f_a.setSize(50), resp1, f"{user_name}", "L", (180, 660))

    resp2 = write_longsh(f_a, resp1, f"体力值： {user_data[1]}/{user_data[4]}", "L", (550, 660))
    resp2 = write_longsh(f_a, resp1, f"健康值： {user_data[2]}/100", "L", (550, 760))
    resp2 = write_longsh(f_a, resp1, f"画境币： {user_data[3]}", "L", (550, 860))
    resp2 = write_longsh(f_a, resp1, f"发言数： {user_data_old[4]}", "L", (550, 1060))
    resp2 = write_longsh(f_a, resp1, f"占位符： 0", "L", (550, 1160))
    resp2 = write_longsh(f_a, resp1, f"占位符： 0", "L", (550, 1260))

    level_txt1 = f"升级到{level_data['now_level']+1}级需要花费{level_data['level_up']}画境币\n发送 升级 即可"

    resp2 = write_longsh(f_a.setSize(35), resp1, level_txt1, "C", (1800, 1800))
    resp2 = resp2.convert("RGB")

    # 压缩图片50%
    s_path = f"""{BASE_PATH}\\cache\\resp_{user_id[0]}.jpg"""
    resp2.save(s_path, optimize=True, quality=50)
    return str(s_path)


# 根据当前行动点上限查找下一级上限
def find_coin_max(now_max: int) -> dict:
    COIN_TABLE = {
            100:50,
            105:100,
            110:200,
            115:300,
            120:500,
            125:1000,
            130:2000,
            135:5000,
            140:7500,
            145:10000,
            150:22500,
            155:40000,
            160:70000,
            165:100000,
            170:120000,
            175:140000,
            180:160000,
            185:180000,
            190:200000,
            195:220000,
            200:240000,
            205:260000,
            210:280000,
            215:300000,
            220:320000,
            225:340000,
            230:360000,
            235:380000,
            240:400000,
            245:420000,
            250:440000,
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