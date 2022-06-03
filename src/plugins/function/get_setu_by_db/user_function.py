'''
Author: 七画一只妖
Date: 2022-06-03 14:35:31
LastEditors: 七画一只妖
LastEditTime: 2022-06-03 15:17:16
Description: file content
'''
import random


from .user_database import get_count, get_data, is_exist
from .user_image import bytes_to_image



# 随机抽取一个图片
def get_image(table_name):
    count = get_count(table_name)
    n = random.randint(0,count)
    data = get_data(table_name, n)
    # image_id = data[0]
    image_bytes = data[1]
    image_name:str = data[2]
    path:str = bytes_to_image(image_bytes, image_name, table_name)
    return image_name, path