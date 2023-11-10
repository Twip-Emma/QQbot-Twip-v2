'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-11-10 14:02:40
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-10 20:04:17
'''
# 用户图鉴生成
from .get_drow import get_pool_dict
from .user_pkg import get_pkg
from .get_image import blend_two_images
from PIL import Image, ImageDraw, ImageFont
import asyncio
import math
import os
from pathlib import Path
import re
import time
loop = asyncio.get_event_loop()


ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
CHAR_PATH: str = f"{ABSOLUTE_PATH}\\char"
TTF_PATH: str = f"{ABSOLUTE_PATH}\\zh-cn.ttf"
PATTERN = re.compile(r'[-\d]+阶|\.[a-zA-Z]+')

char_rare_data = {
    "3阶": "frame50",
    "2阶": "frame20",
    "1阶": "frame5",
    "0阶": "frame1",
    "特殊": "frameX"
}

# 获取图鉴


async def get_user_ill(user_id: str):
    t1 = time.time()
    ill_data, char_name_list = await get_user_pkg(user_id)
    t2 = time.time()
    print(f"获取图鉴耗时：{t2 - t1}")
    img_list = []
    for item in ill_data:
        img_list.append(blend_two_images(
            char_image_path=item[0],
            char_name=str(item[1]),
            char_rank=item[2]
        ))
    t3 = time.time()
    print(f"逐个彩色图片生成耗时：{t3 - t2}")
    img_path = await generate_icon(img_list=img_list, char_name_list=char_name_list, ill_data=ill_data, user_id=user_id)
    t4 = time.time()
    print(f"生成灰色图片与彩色图片进行排序+生成图鉴图片：{t4 - t3}")
    return img_path


# 对背包数据进行处理，生成对应的图片路径列表
async def get_user_pkg(user_id: str) -> list:
    user_pkg = await get_pkg(user_id=user_id)
    char_path_list = []
    char_name_list = []
    for item in user_pkg:
        char_name = item[0]
        char_rank = item[1]
        char_count = int(item[2])
        char_path = ""
        flag = 0

        # 根据角色名称找到对应的图片路径
        char_data = await get_pool_dict()
        for k, v in char_data.items():
            for i in v:
                if char_name in i and char_rank in i:
                    char_path = i
                    flag = 1
                    break
            if flag == 1:
                break

        # 根据碎片数量生成对应的阶级，仅针对0阶、1阶、2阶、3阶角色
        if char_rank in ["0阶角色", "1阶角色", "2阶角色", "3阶角色"]:
            if char_count < 5:
                char_rank = "0阶角色"
            elif char_count < 20:
                char_rank = "1阶角色"
            elif char_count < 50:
                char_rank = "2阶角色"
            else:
                char_rank = "3阶角色"

        if char_count >= 250:
            char_rank = "MAX"

        # 合成返回值
        char_path_list.append([char_path, char_count, char_rank])
        char_name_list.append(char_name)
    return char_path_list, char_name_list


# 生成单角色赋魂图
# 传入：角色图片路径，角色名称，是否为NEW(0/1)
# 返回：Image对象
def blend_two_images(char_image_path, char_name, char_rank):
    rare = ""

    if "3阶" in char_rank:
        rare = char_rare_data["3阶"]
    elif "2阶" in char_rank:
        rare = char_rare_data["2阶"]
    elif "1阶" in char_rank:
        rare = char_rare_data["1阶"]
    elif "0阶" in char_rank:
        rare = char_rare_data["0阶"]
    elif "MAX" in char_rank:
        rare = char_rare_data["特殊"]
    else:
        rare = char_rare_data["3阶"]

    try:
        img1 = Image.open(char_image_path).resize((179, 256)).convert('RGBA')
        img2 = Image.open(f"{ABSOLUTE_PATH}\\icon\\mask_base.png").resize(
            (179, 256)).convert('RGBA')
        img = Image.alpha_composite(img1, img2)

        img3 = Image.open(f"{ABSOLUTE_PATH}\\icon\\{rare}.png").resize(
            (179, 256)).convert('RGBA')
        img = Image.alpha_composite(img, img3)
        img = write_char(char_name, img)
        return img
    except:
        print(f"找不到文件{char_image_path}")
    
    


# 为角色图片上写上角色名字
# 传入：角色名字，背景Image对象
# 返回：写好字的角色图片Image对象
def write_char(char_name, bg):
    # 背景尺寸
    bg_size = (179, 256)

    # 设置字体:路径、字体大小
    font = ImageFont.truetype(TTF_PATH, 18)

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
    draw.text((int((bg_size[0]-text_width[0])/2), 55),
              char_name, fill="#ffffffff", font=font)

    return bg


# 根据结果集生成图鉴
async def generate_icon(img_list: list, char_name_list: list, ill_data: list, user_id:str):
    # 先获取所有角色
    char_data = await get_pool_dict()

    # 结果集
    resp_img_list = []
    resp_img_bg = [0, 0]
    resp_y = []

    for key, value in char_data.items():
        # 1.遍历这一个类型的角色
        icon_list = []
        for v in value:
            # 遍历这一个类型的所有角色，然后判断是否拥有，如果有，则正常拼接图像，如果没有，根据原阶级拼接灰度图
            char_name = re.sub(PATTERN, '', os.path.basename(v))
            if char_name not in char_name_list:
                img_obj = blend_two_images(v, char_name, key)
                # 转换为灰度图
                img_obj = img_obj.convert("L")
                icon_list.append(img_obj)
            else:
                # 正常拼接
                # 由于img_list和ill_data是乱序的，因此需要手动找出对应的图片对象
                index = 0
                for i in char_name_list:
                    if i == char_name:
                        icon_list.append(img_list[index])
                        break
                    index += 1

        # 2.遍历完成后，生成对应的图片
        # 确认画布大小，根据char数量，每行10个char，生成对应长宽的背景
        char_size = (179, 256)
        char_count = len(value)
        bg_w = 0
        bg_h = 0
        if char_count >= 0:
            bg_w = char_size[0] * 10
        else:
            bg_w = char_size[0] * char_count

        if char_count <= 10:
            bg_h = char_size[1]
        else:
            bg_h = char_size[1] * math.ceil(char_count / 10)

        # bg颜色为#0a272a
        bg_size = (bg_w, bg_h)
        bg = Image.new("RGBA", bg_size, (10, 39, 42, 255))

        # 遍历icon_list把每个元素依次贴到bg上面，每10个一行
        x = 0
        y = 0
        for i in range(0, len(icon_list)):
            bg.paste(icon_list[i], (x, y), mask=icon_list[i])
            x += char_size[0]
            if (i + 1) % 10 == 0:
                # 换行操作
                y += char_size[1]
                x = 0

        # 生成标题背景，文字上下左右居中
        title_size = (bg_w, 80)
        title_bg = Image.new("RGBA", title_size, (10, 39, 42, 255))

        font = ImageFont.truetype(TTF_PATH, 60)
        text_width = font.getsize(key)
        draw = ImageDraw.Draw(title_bg)

        # 写字
        draw.text((int((title_size[0]-text_width[0])/2), int((title_size[1] -
                  text_width[1])/2)), key, fill="#FFFF00", font=font)
        
        # 把bg和title_bg上下拼接在一起
        resp = Image.new("RGBA", (bg_size[0], bg_size[1] + title_size[1]), (10, 39, 42, 255))
        resp.paste(title_bg, (0, 0))
        resp.paste(bg, (0, 80))

        # 累计记录图片高度以及每组图鉴的图像对象，为最后合成图片做准备
        resp_y.append(resp_img_bg[1])
        if bg_size[0] > resp_img_bg[0]:
            resp_img_bg[0] = bg_size[0]
        resp_img_bg[1] += bg_size[1] + title_size[1]
        resp_img_list.append(resp)
        

    # 最后合成图片
    result = Image.new("RGBA", (resp_img_bg[0], resp_img_bg[1]), (10, 39, 42, 255))
    index = 0
    for img in resp_img_list:
        result.paste(img, (0, resp_y[index]), mask=img)
        index += 1

    # 保存图片并返回路径
    save_path = f"{ABSOLUTE_PATH}\\cache\\{user_id}_图鉴.jpg"
    result = result.convert("RGB")
    result.save(save_path, quality=50)
    return save_path

