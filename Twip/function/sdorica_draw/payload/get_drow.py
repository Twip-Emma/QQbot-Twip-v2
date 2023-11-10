import datetime
import os
import random
import re
from pathlib import Path
from .user_pkg import add_pkg, get_pkg
from .get_image import get_img_result
from .db import sql_dql

ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
CHAR_PATH: str = f"{ABSOLUTE_PATH}\\char"
PATTERN = re.compile(r'[-\d]+阶|\.[a-zA-Z]+')

# 每日抽卡次数
PULL_NUM = 5


# 抽卡流程
async def drow(user_id: str):
    # 判断是否有抽卡次数
    if not await check_user_pull(user_id):
        return None
    
    # 获取卡池数据字典
    pool_dict = await get_pool_dict()

    # 获取抽卡结果
    result = await get_draw_result(pool_dict)

    # 获取is_new列表
    is_new_list = await is_new(result, await get_pkg(user_id))

    # 添加抽卡数据
    await add_data(data=result, user_id=user_id)

    # 合成并返回图片结果
    return await get_img_result(data=result, is_new_list=is_new_list, user_id=user_id)



# 获取卡池的数据字典
async def get_pool_dict() -> dict:
    # 初始化一个空字典来存储数据
    image_dict = {}

    # 遍历父文件夹下的所有子文件夹
    for subfolder in os.listdir(CHAR_PATH):
        subfolder_path = os.path.join(CHAR_PATH, subfolder)

        # 检查子文件夹是否是一个目录
        if os.path.isdir(subfolder_path):
            # 初始化一个空列表来存储子文件夹中的图片文件
            image_list = []

            # 遍历子文件夹中的所有文件
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)

                # 检查文件是否是图片文件（你可以根据需要添加更多的图片文件扩展名）
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    image_list.append(file_path)

            # 将子文件夹名称作为键，图片文件列表作为值存入字典
            image_dict[subfolder] = image_list
    return image_dict


# 合成抽卡结果
async def get_draw_result(image_dict: dict) -> list:
    drow_list = []
    drow_list_tmp = []
    for i in range(10):
        index = random.randint(0, 100)
        if index <= 3:
            drow_list_tmp.append(random.choice(["群友角色", "mz角色", "sp角色"]))
        elif index <= 10:
            drow_list_tmp.append("2阶角色")
        elif index <= 20:
            drow_list_tmp.append("1阶角色")
        else:
            drow_list_tmp.append("0阶角色")

    for key in drow_list_tmp:
        char = random.choice(image_dict[key])
        drow_list.append(
            [
                key,
                char,
                re.sub(PATTERN, '', os.path.basename(char))
            ]
        )

    return drow_list


# 往背包里面添加数据
async def add_data(data: list, user_id: int):
    for item in data:
        await add_pkg(user_id, item[2], item[0])


# 获取是否为new的抽卡列表
async def is_new(data: list, user_pkg: list) -> bool:
    character_list = [i[2] for i in data] # 抽卡结果
    pkg_list = [i[0] for i in user_pkg] # 用户背包

    is_new_dict = {}  # 用于跟踪每个角色第一次出现的索引
    is_new_list = []  # 存储 is_new 值

    # 检查每个角色是否是用户背包数据中出现过的
    for i, character in enumerate(character_list):
        if character in is_new_dict or character in pkg_list:
            is_new_list.append(1)
        else:
            is_new_list.append(0)
            is_new_dict[character] = i

    return is_new_list


# 校验该用户是否还有抽卡次数
async def check_user_pull(user_id: int) -> bool:
    re = await sql_dql(
        "select count(*) from user_pkg where drow_time=? and user_id=?",
        (
            datetime.datetime.now().strftime("%Y-%m-%d"),
            user_id
        )
    )
    if int(re[0][0]) >= PULL_NUM * 10:
        return False
    else:
        return True