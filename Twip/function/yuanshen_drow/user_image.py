'''
Author: 七画一只妖
Date: 2021-11-10 15:33:09
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 16:31:11
Description: file content
'''
from PIL import Image, ImageFont, ImageDraw, ImageMath

# 同级
from .user_config import FILE_PATH


# 获取一个抽卡角色的图像
async def get_image(name,star,i_type,is_new):
    name = name + "-" + star + "-" + i_type

    _weap_chack = ["单手剑","双手剑","弓","枪","法器"]
    if is_new == "0":
        bg = Image.open(f"{FILE_PATH}\\_icon\\{star}x_new.png")  # 打开边框
    elif is_new == "1":
        bg = Image.open(f"{FILE_PATH}\\_icon\\{star}x_old.png")  # 打开边框
    bg_b = bg.resize((320, 2400))
    bg_b = bg_b.convert('RGBA')

    if i_type in _weap_chack:
        avatar_icon = Image.open(f"{FILE_PATH}\\icon\\_武器\\{name}.png")  # 打开角色预设图
        # avatar_icon = Image.open(f"{FILE_PATH}\\gacha_image\\角色\\{name}.png")
    else:
        avatar_icon = Image.open(f"{FILE_PATH}\\icon\\_图鉴\\{name}.png")  # 打开角色预设图
    avatar_icon = avatar_icon.resize((320, 2400))
    avatar_icon = avatar_icon.convert('RGBA')

    back = Image.open(f"{FILE_PATH}\\icon\\{star}_star_bg.png")  # 打开背景
    back = back.resize((320, 2400))
    back = back.convert('RGBA')

    avatar_icon = Image.alpha_composite(avatar_icon, bg_b)
    avatar_icon = Image.alpha_composite(back, avatar_icon)

    # 完成角色图与边框图拼合后，进行星级和属性的拼合
    # 处理属性图标
    element_icon = Image.open(f"{FILE_PATH}\\icon\\{i_type}.png")  # 获取对应属性图标
    element_icon = element_icon.resize((200, 200))
    x = int((320-element_icon.width)/2)
    y = 1500
    avatar_icon.paste(element_icon, (x, y), element_icon)
    # 处理星级图标
    star_icon = Image.open(f"{FILE_PATH}\\icon\\{star}_star.png")  # 获取对应属性图标
    star_icon = star_icon.resize((star_icon.width*2, star_icon.height*2))
    x = int((320-star_icon.width)/2)
    y = 1690
    avatar_icon.paste(star_icon, (x, y), star_icon)
    return avatar_icon

