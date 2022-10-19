'''
Author: 七画一只妖
Date: 2022-03-16 18:45:52
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-19 15:28:31
Description: file content
'''
import random
from PIL import Image
import base64
from io import BytesIO
import os


from .function_pkg import get_pool_info,removal1,ten_blue
from .user_package import attack_chack, select_user_pack
from .get_image import get_png_path,blend_two_images,finally_get_image

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


# 主控室
def start(user_id,pool_name) -> str:

    # 抽卡次数判断
    bool_r, time, total, sptotal = attack_chack(user_id)
    if not bool_r:
        return f"""【Error】你的发言小于{total},有{time}次抽卡机会，现已用完\n你的发言总数：{sptotal}"""

    # 根据名称抽卡
    char_list, char_name_list = get_pool_info(pool_name)
    img_class = []
    is_new = removal1(char_name_list)
    is_new = select_user_pack(char_name_list,is_new,user_id)

    # 10抽保底蓝
    if "1阶" not in str(char_name_list) and "2阶" not in str(char_name_list) and "3阶" not in str(char_name_list) and "SP" not in str(char_name_list) or "MZ" not in str(char_name_list) and "X阶" not in str(char_name_list):
        b = random.randint(0,9)
        char_name_list[b] = ten_blue()
        char_list[b] = get_png_path(char_name_list[b])

    for (item,char_name,new) in zip(char_list,char_name_list,is_new):
        img_class.append(blend_two_images(item,char_name,new))

    bg = finally_get_image(img_class,user_id)

    # 保存图片到images文件夹
    bg.save(f"{FILE_PATH}/image/{user_id}.jpg")

    # 获取图片路径
    cq = f"file:///{FILE_PATH}/image/{user_id}.jpg"

    return cq


# def img_to_b64(pic: Image.Image) -> str:
#     buf = BytesIO()
#     pic.save(buf, format="PNG")
#     base64_str = base64.b64encode(buf.getbuffer()).decode()
#     return "base64://" + base64_str