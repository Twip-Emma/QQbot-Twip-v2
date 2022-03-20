'''
Author: 七画一只妖
Date: 2022-03-20 14:16:15
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 16:31:19
Description: file content
'''
import copy
import random
from PIL import Image, ImageFont, ImageDraw, ImageMath


# 同级
from .data.pool_info import *
from .user_image import get_image



# 去重函数，传入角色+等阶的列表，返回一个是否为new的0/1列表
# 0是new，1是重复
async def removal1(char_name_list):
    # print("函数内去重前角色列表：",char_name_list)
    is_new = ["0","0","0","0","0","0","0","0","0","0"] # 定义0、1列表
    x = 0 # 扫描的索引值
    char_name_list_p = copy.deepcopy(char_name_list)
    for char in char_name_list:
        # print(char_name_list_p)
        char_name_list_p[x] = "==="
        y = 0
        for item in char_name_list_p:
            if item == char:
                is_new[y] = "1"
            y += 1
        x += 1

    return is_new


#######################################################
# 根据随机数，生成结果列表
async def get_result() -> list:
    i = 0 
    my_list = []
    while(i<10):
        flag = random.randint(1,1000)
        if flag <= 200:
            item = random.choices(update_pool_5x)
        elif flag <= 400:
            item = random.choices(weap_pool_5x)
        elif flag <= 600:
            item = random.choices(update_pool_4x)
        elif flag <= 800:
            item = random.choices(weap_pool_4x)
        else:
            item = random.choices(weap_pool_3x)
        my_list.append(item)
        i += 1
    return my_list


#######################################################
# 判断保底（仅十连）
async def is_safe(my_list:list) -> list:
    flag = False
    for item in my_list:
        if item[0]["star"] == "4" or item[0]["star"] == "5":
            flag = True
            break
    if flag == False:
        index = random.randint(0,10)
        char = random.choices(update_pool_4x)
        my_list[index] = char
    return my_list


#######################################################
# 将人物卡向左移
async def left_shift(my_list) -> list:
    weap_list = ["单手剑","双手剑","弓","枪","法器"]
    i2 = 0
    while i2 < 10:
        i3 = 0
        while i3 < 9:
            if (my_list[i3][0]["type"] in weap_list) and (my_list[i3 + 1][0]["type"] not in weap_list):
                my_list[i3],my_list[i3 + 1] = my_list[i3 + 1],my_list[i3]
            i3 += 1
        i2 += 1
    return my_list


#######################################################
# 将高星卡向左移
async def left_shift_high_star(my_list) -> list:
    # i2 = 0
    # while i2 < 10:
    #     i3 = 0
    #     while i3 < 9:
    #         if my_list[i3][0]["star"] == "5" and my_list[i3 + 1][0]["star"] != "5":
    #             my_list[i3],my_list[i3 + 1] = my_list[i3 + 1],my_list[i3]
    #         i3 += 1
    #     i2 += 1
    # return my_list
    i2 = 0
    while i2 < 10:
        i3 = 0
        while i3 < 9:
            if (my_list[i3][0]["star"] == "4" and my_list[i3 + 1][0]["star"] == "5") or \
            (my_list[i3][0]["star"] == "3" and my_list[i3 + 1][0]["star"] == "5") or \
            (my_list[i3][0]["star"] == "3" and my_list[i3 + 1][0]["star"] == "4"):
                my_list[i3],my_list[i3 + 1] = my_list[i3 + 1],my_list[i3]
            i3 += 1
        i2 += 1
    return my_list


#######################################################
# 判断结果列表中的重复项，并且从第二个开始标记
async def is_repeat(my_list) -> list:
    # i = 0
    # while i < 9:
    #     if my_list[i][0]["name"] == my_list[i + 1][0]["name"]:
    #         my_list[i][1] = "1"
    #     i += 1
    # return my_list
    char_name_list = []
    for item in my_list:
        char_name_list.append(item[0]["name"])
    is_new = await removal1(char_name_list)
    return is_new


#######################################################
# 根据每个结果获取对应Image对象
async def get_image_list(my_list,is_new) -> list:
    p = 0
    image_list = []
    for item in my_list:
        name = item[0]["name"]
        star = item[0]["star"]
        type = item[0]["type"]
        image = await get_image(name,star,type,is_new[p])
        image_list.append(image)
        p += 1
    return image_list


#######################################################
# 拼合这十个Image对象
async def get_final_image(image_list) -> Image:
    i = 0
    bg_img = Image.new("RGBA", (3200, 2400), (255, 255, 255))
    for image_item in image_list:
        x = int(i * 320)
        y = 0
        bg_img.paste(image_item, (x, y), image_item)
        i += 1
    return bg_img


#######################################################
# 将list中相同的元素放在一起
# async def get_final_list(my_list) -> list:
#     final_list = []
#     for item in my_list:
#         if item[1] == "1":
#             final_list.append(item[0])
#     return final_list