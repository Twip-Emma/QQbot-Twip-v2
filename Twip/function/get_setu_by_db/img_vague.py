'''
Author: 七画一只妖
Date: 2022-06-05 19:09:57
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 10:57:09
Description: file content
'''
'''
Author: 七画一只妖
Date: 2022-05-30 14:52:17
LastEditors: 七画一只妖
LastEditTime: 2022-05-30 17:55:19
Description: file content
'''
import random
from pathlib import Path

from PIL import Image

BASE_PATH: str = Path(__file__).absolute().parents[0]
IMG_PATH = f'{BASE_PATH}\\images'


# 黑块大小
BIOCK_SIZE = 50


# 将图片切割成(100, 100)的小块并记录每一个小块的左上角坐标，返回一个列表
def cut_img(img_path):
    img = Image.open(img_path)
    width, height = img.size
    # 切割的起始坐标
    start_x = 0
    start_y = 0
    # 切割的结束坐标
    end_x = BIOCK_SIZE
    end_y = BIOCK_SIZE
    # 切割的小块的左上角坐标
    cut_list = []
    while start_y < height:
        while start_x < width:
            cut_list.append((start_x, start_y))
            start_x += BIOCK_SIZE
            end_x += BIOCK_SIZE
        start_x = 0
        end_x = BIOCK_SIZE
        start_y += BIOCK_SIZE
        end_y += BIOCK_SIZE
    return cut_list


# 传入一个列表和百分比，根据百分比选择列表中的元素，返回一个列表
def random_list(list_data , percent):
    random_list = []
    for i in range(int(len(list_data) * percent)):
        random_list.append(random.choice(list_data))
    return random_list



# 传入一个坐标列表和图片路径，根据100X100的大小，涂黑图片
def paint_black(cut_list, img_path):
    block_size = (BIOCK_SIZE, BIOCK_SIZE)
    img = Image.open(img_path)

    # 生成黑色区域
    black_img = Image.new('RGB', block_size, (0, 0, 0))

    # 将black_img粘贴到img上
    for i in cut_list:
        img.paste(black_img, i)
    
    return img




# 主控
def img_format_main(percent, input_path:str, output_path:str) -> str:
    img = paint_black(random_list(cut_img(input_path),percent), input_path)
    img.save(output_path)
    return output_path