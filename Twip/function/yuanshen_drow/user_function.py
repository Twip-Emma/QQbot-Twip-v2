'''
Author: 七画一只妖
Date: 2022-03-20 14:13:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 14:21:51
Description: file content
'''
import random
import time
from PIL import Image, ImageFont, ImageDraw, ImageMath
from Twip import TTF_PATH


# 同级
from .user_utils import get_result, is_safe, left_shift, left_shift_high_star, is_repeat, get_image_list, get_final_image
from .user_config import FILE_PATH


# 主控
# 抽卡主控，直接和用户交互
async def chouka_start(user_id, user_name, time_gacha) -> str:
    t1 = time.time()
    #######################################################
    # 根据随机数，生成结果列表
    my_list = await get_result()

    #######################################################
    # 判断保底（仅十连）
    my_list = await is_safe(my_list=my_list)

    #######################################################
    # 将人物卡向左移
    my_list = await left_shift(my_list=my_list)

    #######################################################
    # 将高星卡向左移
    my_list = await left_shift_high_star(my_list=my_list)

    #######################################################
    # 判断结果列表中的重复项，并且从第二个开始标记，返回新旧列表
    is_new = await is_repeat(my_list=my_list)

    #######################################################
    # 根据每个结果获取对应Image对象
    image_list = await get_image_list(my_list=my_list, is_new=is_new)

    #######################################################
    # 拼合这十个Image对象
    bg_img = await get_final_image(image_list=image_list)

    # 创建背景
    bg_img = bg_img.resize((2320, 1712))
    # finally_bg
    bg_finally = Image.open(f"{FILE_PATH}\\_icon\\finally_bg.png")
    bg_finally = bg_finally.resize((3044, 1712))
    # bg_finally = Image.new("RGB",(3044,1712),(0,0,0))
    bg_finally.paste(bg_img, (362, 0), bg_img)

    t2 = time.time()
    t = "{:.2f}".format(t2-t1)

    # 写字
    font_size = 40
    text = f"{user_name} 的抽卡结果       QQID：{user_id}       剩余抽卡次数：{time_gacha} \
    \n\nBy七画一只妖，拼合图像耗时：{t}秒"
    font_path = TTF_PATH
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(bg_finally)
    text_coordinate = int(100), int(bg_finally.height - 180)
    draw.text(text_coordinate, text, fill="#ffffffff", font=font)

    # 要保存图片的路径
    # bg_finally = small_image(bg_finally)
    img_path = f'{FILE_PATH}\\image\\{user_id[0]}.jpg'
    # 保存图片
    bg_finally = bg_finally.convert("RGB")
    bg_finally.save(img_path)

    return img_path
