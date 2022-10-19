'''
Author: 七画一只妖
Date: 2021-09-08 21:19:15
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-19 15:25:36
Description: file content
'''
import os
from io import BytesIO
import base64
from .user_package import *

from PIL import Image, ImageDraw, ImageFont
from Twip import ABSOLUTE_PATH


FILE_PATH = ABSOLUTE_PATH + "\\function\\sdorica_draw"
ICON_PATH = ABSOLUTE_PATH + "\\function\\sdorica_draw\\char"


char_rare_data = {
    "3阶": "frame50",
    "2阶": "frame20",
    "1阶": "frame5",
    "0阶": "frame1",
    "特殊": "frameX"
}


def get_png_path(name):
    # 获取png文件路径，传入的参数是角色或武器名字，会自动在角色和武器文件夹搜索，找不到抛出异常
    # 检索路径为次文件同级的icon文件夹下名为角色图鉴或角色图鉴文件夹内的所有图片
    # 可根据自己实际情况取舍

    # arms_name_path = os.path.join(ICON_PATH, "sp角色", str(name) + ".png")
    # role_name_path3 = os.path.join(ICON_PATH, "3阶角色", str(name) + ".png")
    # role_name_path2 = os.path.join(ICON_PATH, "2阶角色", str(name) + ".png")
    # role_name_path1 = os.path.join(ICON_PATH, "1阶角色", str(name) + ".png")
    # role_name_path0 = os.path.join(ICON_PATH, "0阶角色", str(name) + ".png")
    # role_name_pathx = os.path.join(ICON_PATH, "特殊角色", str(name) + ".png")
    # role_name_pathxx = os.path.join(ICON_PATH, "群友角色", str(name) + ".png")
    # role_name_pathmz = os.path.join(ICON_PATH, "mz角色", str(name) + ".png")

    if "0阶" in name:
        return os.path.join(ICON_PATH, "0阶角色", str(name) + ".png")
    elif "1阶" in name:
        return os.path.join(ICON_PATH, "1阶角色", str(name) + ".png")
    elif "2阶" in name:
        return os.path.join(ICON_PATH, "2阶角色", str(name) + ".png")

    arms_name_path = os.path.join(ICON_PATH, "sp角色", str(name) + ".png")
    role_name_path3 = os.path.join(ICON_PATH, "3阶角色", str(name) + ".png")
    role_name_pathx = os.path.join(ICON_PATH, "特殊角色", str(name) + ".png")
    role_name_pathxx = os.path.join(ICON_PATH, "群友角色", str(name) + ".png")
    role_name_pathmz = os.path.join(ICON_PATH, "mz角色", str(name) + ".png")

    if os.path.exists(role_name_path3):
        return role_name_path3

    if os.path.exists(arms_name_path):
        return arms_name_path

    if os.path.exists(role_name_pathx):
        return role_name_pathx

    if os.path.exists(role_name_pathxx):
        return role_name_pathxx

    if os.path.exists(role_name_pathmz):
        return role_name_pathmz

    raise FileNotFoundError(f"找不到 {name} 的图标，请检查图标是否存在")


# 生成单角色赋魂图
# 传入：角色图片路径，角色名称，是否为NEW(0/1)
# 返回：Image对象
def blend_two_images(char_image_path, char_name_list, new):
    rare = ""

    if "3阶" in char_image_path or "MZ" in char_image_path or "SP" in char_image_path:
        rare = char_rare_data["3阶"]
    elif "2阶" in char_image_path:
        rare = char_rare_data["2阶"]
    elif "1阶" in char_image_path:
        rare = char_rare_data["1阶"]
    elif "0阶" in char_image_path:
        rare = char_rare_data["0阶"]
    elif "X阶" in char_image_path:
        rare = char_rare_data["特殊"]

    img1 = Image.open(char_image_path).resize((179, 256)).convert('RGBA')
    img2 = Image.open(f"{FILE_PATH}\\icon\\mask_base.png").resize(
        (179, 256)).convert('RGBA')
    img = Image.alpha_composite(img1, img2)

    img3 = Image.open(f"{FILE_PATH}\\icon\\{rare}.png").resize(
        (179, 256)).convert('RGBA')
    img = Image.alpha_composite(img, img3)

    # 判断是否为new
    if new == "0":
        img4 = Image.open(f"{FILE_PATH}\\icon\\new.png").resize(
            (179, 256)).convert('RGBA')
        img = Image.alpha_composite(img, img4)
    img = write_char(char_name_list, img)
    return img


# 合成结算界面
# 传入：合成后的单图片Image对象的列表，用户QQ号
# 返回：无
# 将结果保存在同级目录下的image文件夹内，以用户QQ号命名
def finally_get_image(img_class, user_id) -> Image.Image:
    bg_size = (2160, 1080)
    bg_path = os.path.join(f'{FILE_PATH}\\icon\\base.png')
    bg = Image.open(bg_path).convert('RGBA')

    fruit_size = (305, 423)  # 角色图尺寸声明
    x, y = 407, 166  # 第一抽角色图片左上角的点定位

    width_more = 0
    line_mach = 1
    for item in img_class:
        fruit = item.resize(fruit_size)
        fruit_box = (x + width_more, y, (x + width_more +
                     fruit_size[0]), (y + fruit_size[1]))
        bg.paste(fruit, fruit_box, fruit)
        width_more += 260  # 每一抽右移动244像素
        line_mach += 1

        if line_mach == 6:
            y += 320  # 第二行是下移动388像素
            width_more = 0

    # 写字
    text = "用户QQ ID: " + user_id
    bg = add_text(bg, text)

    # 保存图片
    bg = bg.convert('RGB')
    return bg


# 为角色图片上写上角色名字
# 传入：角色名字，背景Image对象
# 返回：写好字的角色图片Image对象
def write_char(char_name, bg):
    # 移除角色昵称中，多余的字
    x = char_name.split("-")
    char_name = x[0]
    if "MZ" in char_name:
        char_name = char_name.replace(" 拷贝", "")
    if "SP" in char_name:
        char_name = char_name.replace(" 拷贝", "")

    # 背景尺寸
    bg_size = (179, 256)

    # 设置字体:路径、字体大小
    font = ImageFont.truetype(os.path.join(f"{FILE_PATH}\\zh-cn.ttf"), 18)

    # 计算使用该字体占据的空间
    # 返回一个 tuple (width, height)
    # 分别代表这行字占据的宽和高
    text_width = font.getsize(char_name)
    draw = ImageDraw.Draw(bg)

    # 计算字体位置
    # 下面这个是上下左右居中
    # text_coordinate = int((bg_size[0]-text_width[0])/2), int((bg_size[1]-text_width[1])/2)
    # 抽卡只需要左右居中显示文字即可
    # text_coordinate = int((bg_size[0]-text_width[0])/2), 55

    # 写字
    draw.text((int((bg_size[0]-text_width[0])/2), 55), char_name, fill="#ffffffff", font=font)

    # 要保存图片的路径
    # img_path = os.path.join(f'center_text.jpg')
    # # 保存图片
    # bg.save(img_path)
    # print('保存成功 at {}'.format(img_path))

    return bg


# 在图片下方添加文字
def add_text(bg, text):
    # 背景尺寸
    bg_size = (2160, 1080)

    # 设置字体
    font = ImageFont.truetype(os.path.join(f"{FILE_PATH}\\zh-cn.ttf"), 30)

    # 计算使用该字体占据的空间
    # 返回一个 tuple (width, height)
    # 分别代表这行字占据的宽和高
    text_width = font.getsize(text)
    draw = ImageDraw.Draw(bg)

    # 计算字体位置
    # 下面这个是上下左右居中
    # text_coordinate = int((bg_size[0]-text_width[0])/2), int((bg_size[1]-text_width[1])/2)
    # 抽卡只需要左右居中显示文字即可
    text_coordinate = int((bg_size[0]-text_width[0])/2), int(120)

    # 写字
    draw.text(text_coordinate, text, fill="#ffffffff", font=font)

    return bg


# 把传进来的Image对象转成base64
# def pic2b64(im):
#     bio = BytesIO()
#     im.save(bio, format='PNG')
#     base64_str = base64.b64encode(bio.getvalue()).decode()
#     return 'base64://' + base64_str


# 优化
# 1.压缩图片
# def small_image(im):
#     width = im.size[0]   # 获取宽度
#     height = im.size[1]   # 获取高度
#     img = im.resize((int(width*0.3), int(height*0.3)), Image.ANTIALIAS)
#     return img
