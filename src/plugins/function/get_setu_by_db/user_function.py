'''
Author: 七画一只妖
Date: 2022-06-03 14:35:31
LastEditors: 七画一只妖
LastEditTime: 2022-06-05 20:14:42
Description: file content
'''
import random


from .user_database import get_count, get_data, is_exist
from .user_image import bytes_to_image, img_vague


from tool.database_handle.user_info_new import get_user_health, is_exist_user_info_new, insert_user_info_new, reduce_user_health


IMAGE_VAGUE = {
    100: 0,
    95: 0.05,
    90: 0.1,
    85: 0.2,
    80: 0.3,
    75: 0.4,
    70: 0.5,
    65: 0.6,
    60: 0.8,
    55: 1,
    50: 1.5,
    40: 2,
    30: 2.5,
    20: 3,
    10: 3.5,
    0: 4
}

# 随机抽取一个图片
def get_image(table_name,user_id):
    count = get_count(table_name)
    n = random.randint(0,count)
    data = get_data(table_name, n)
    # image_id = data[0]
    image_bytes = data[1]
    image_name:str = data[2]
    path:str = bytes_to_image(image_bytes, image_name, table_name)
    if not is_exist_user_info_new(user_id):
        insert_user_info_new(user_id)

    user_health = get_user_health(user_id)

    # 根据IMAGE_VAGUE查找对应user_health的值
    vague_percent = 5
    for key in IMAGE_VAGUE:
        if user_health >= key:
            vague_percent = IMAGE_VAGUE[key]
            break

    path = img_vague(vague_percent, path, path)
    reduce_user_health(user_id, 3)
    user_health = get_user_health(user_id)
    return image_name, path, user_health