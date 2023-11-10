import os
from PIL import Image, ImageDraw, ImageFont
# from Twip import ABSOLUTE_PATH, TTF_PATH

from pathlib import Path
ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
TTF_PATH: str = f"{ABSOLUTE_PATH}\\zh-cn.ttf"


char_rare_data = {
    "3阶": "frame50",
    "2阶": "frame20",
    "1阶": "frame5",
    "0阶": "frame1"
}


# 获取结果
async def get_img_result(data:list, is_new_list:list, user_id:str):
    index = 0
    img_obj_list = []
    for item in data:
        img_obj_list.append(blend_two_images(
            char_image_path=item[1],
            char_name=item[2],
            new=is_new_list[index]
        ))
        index += 1
    bg = finally_get_image(img_class=img_obj_list, user_id=user_id)
    # 保存图片并返回路径
    bg.save(f"{ABSOLUTE_PATH}\\cache\\{user_id}.jpg")
    return f"{ABSOLUTE_PATH}\\cache\\{user_id}.jpg"
    


# 生成单角色赋魂图
# 传入：角色图片路径，角色名称，是否为NEW(0/1)
# 返回：Image对象
def blend_two_images(char_image_path, char_name, new):
    rare = ""

    if "3阶" in char_image_path or "MZ" in char_image_path or "SP" in char_image_path or "X阶" in char_image_path:
        rare = char_rare_data["3阶"]
    elif "2阶" in char_image_path:
        rare = char_rare_data["2阶"]
    elif "1阶" in char_image_path:
        rare = char_rare_data["1阶"]
    elif "0阶" in char_image_path:
        rare = char_rare_data["0阶"]
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
    

        # 判断是否为new
        if new == 0:
            img4 = Image.open(f"{ABSOLUTE_PATH}\\icon\\new.png").resize(
                (179, 256)).convert('RGBA')
            img = Image.alpha_composite(img, img4)
        img = write_char(char_name, img)
        return img
    except:
        print(f"找不到文件{char_image_path}")
    


# 合成结算界面
# 传入：合成后的单图片Image对象的列表，用户QQ号
# 返回：结果的图片对象
def finally_get_image(img_class, user_id) -> Image.Image:
    bg_size = (2160, 1080)
    bg_path = os.path.join(f'{ABSOLUTE_PATH}\\icon\\base.png')
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


# 在图片下方添加文字
def add_text(bg, text):
    # 背景尺寸
    bg_size = (2160, 1080)

    # 设置字体
    font = ImageFont.truetype(TTF_PATH, 30)

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
