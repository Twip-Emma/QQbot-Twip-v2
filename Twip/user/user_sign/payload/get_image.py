from PIL import Image, ImageDraw, ImageFont

import random

from .db import sql_dml, sql_dql
import datetime
import uuid
from pathlib import Path
ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]
TTF = f'{ABSOLUTE_PATH}\\zh-cn.ttf'


# 绘制背景
def draw_circles(image):
    draw = ImageDraw.Draw(image)

    # 定义圆的半径和圆心之间的距离
    radius = 5
    distance = 100

    # 设置第一个小圆点的圆心位置为(50, 50)
    center_x = 100
    center_y = 100

    # 在图片上均匀分布10x10个白色小圆点
    for i in range(9):
        for j in range(9):
            # 计算每个小圆点的圆心坐标
            current_x = center_x + i * distance
            current_y = center_y + j * distance

            # 绘制白色小圆点
            draw.ellipse(
                [
                    (current_x - radius, current_y - radius),
                    (current_x + radius, current_y + radius)
                ],
                fill=(255, 255, 255)
            )
    return image


# 写字
async def draw_bg():
    # 创建一个黑色背景的图片
    width, height = 1000, 1000
    background_color = (0, 0, 0)
    image = Image.new("RGB", (width, height), background_color)

    # 调用绘制圆点的函数
    draw = ImageDraw.Draw(draw_circles(image))

    # 定义字体和文字
    font_path = TTF  # 替换为你的字体文件路径
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # 定义文字列表
    characters = ["青", "白", "朱", "玄", "南", "参", "北", "玉"]

    # 定义字往右下角偏移的值
    drift = 5

    # 记录已绘制文字的坐标
    drawn_coordinates = set()

    # 定义固定字的坐标
    draw.text((500 + drift, 500 + drift), "空", font=font, fill=(255, 255, 255))
    drawn_coordinates.add((500 + drift, 500 + drift))
    draw.text((100 + drift, 100 + drift), "吉", font=font, fill=(255, 255, 255))
    drawn_coordinates.add((100 + drift, 100 + drift))
    draw.text((900 + drift, 100 + drift), "平", font=font, fill=(255, 255, 255))
    drawn_coordinates.add((900 + drift, 100 + drift))
    draw.text((100 + drift, 900 + drift), "诡", font=font, fill=(255, 255, 255))
    drawn_coordinates.add((100 + drift, 900 + drift))
    draw.text((900 + drift, 900 + drift), "厄", font=font, fill=(255, 255, 255))
    drawn_coordinates.add((900 + drift, 900 + drift))


    # 判断当日是否生成了文字坐标
    character_data = await sql_dql(
        "select sign from user_sign where user_id=? and time=?",
        (
            "系统",
            datetime.datetime.now().strftime("%Y-%m-%d")
        )
    )
    if character_data != []:
        point_list = parse_coordinates_string(character_data[0][0])
        for index in range(len(characters)):
            draw.text((point_list[index][0], point_list[index][1]), characters[index], font=font, fill=(255, 255, 255))
    else:
        add_list = []
        for character in characters:
            while True:
                # 随机选择一个位置
                x = random.randint(1, 8) * 100 + drift
                y = random.randint(1, 8) * 100 + drift

                # 如果该位置未被占用，则绘制文字并跳出循环
                if (x, y) not in drawn_coordinates:
                    drawn_coordinates.add((x, y))
                    add_list.append((x, y))
                    draw.text((x, y), character, font=font, fill=(255, 255, 255))
                    break
        await sql_dml(
            "insert into user_sign (id, user_id, time, sign)values(?,?,?,?)",
            (
                str(uuid.uuid4()),
                "系统",
                datetime.datetime.now().strftime("%Y-%m-%d"),
                str(add_list)
            )
        )
    
    return image


# 在两个点之间画线段
def draw_line_between_points(image, point1, point2):
    draw = ImageDraw.Draw(image)

    # 定义直线颜色和宽度
    line_color = (255, 255, 255)
    line_width = 6

    # 绘制直线
    draw.line([point1, point2], fill=line_color, width=line_width)
    return image


# 随机生成路径
def generate_random_circle_coordinates():
    # 定义相邻圆点的相邻位置
    neighbor_positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # 定义初始点和存储生成的圆点坐标
    initial_point = (500, 500)
    circle_coordinates = [initial_point]

    used_coordinates = set([initial_point])

    for _ in range(30):
        # 从相邻位置中随机选择下一个点
        next_position = random.choice(neighbor_positions)

        # 计算下一个点的坐标
        next_x = circle_coordinates[-1][0] + next_position[0] * 100
        next_y = circle_coordinates[-1][1] + next_position[1] * 100

        # 将坐标限制在[100, 900]的范围内
        next_x = max(99, min(next_x, 901))
        next_y = max(99, min(next_y, 901))

        # 如果下一个坐标已经被使用，则回到中心坐标
        if (next_x, next_y) in used_coordinates:
            next_x, next_y = initial_point

        # 将下一个点添加到列表中
        circle_coordinates.append((next_x, next_y))
        used_coordinates.add((next_x, next_y))

    return circle_coordinates


# 写字
def write_char(char_name, bg):
    bg_size = (1000, 1000)
    font = ImageFont.truetype(TTF, 50)
    text_width = font.getsize(char_name)
    draw = ImageDraw.Draw(bg)

    # 写字
    draw.text((int((bg_size[0]-text_width[0])/2), 925),
              char_name, fill="#ffffffff", font=font)
    return bg


# 数据转换-str转list
def parse_coordinates_string(coordinates_string):
    # 移除首尾的方括号，并按逗号分隔字符串
    coordinates_list = coordinates_string.strip('[]').replace("(","").replace(")","").split(",")

    # 提取每个坐标点的 x 和 y，并转换为整数
    parsed_coordinates = [(int(coordinates_list[i]), int(coordinates_list[i + 1])) for i in range(0, len(coordinates_list), 2)]

    return parsed_coordinates


# 获取签到图
async def get_sign_image(user_id: str, user_name: str, random_circle_coordinates: list = None):
    if not random_circle_coordinates:
        random_circle_coordinates = generate_random_circle_coordinates()
        await sql_dml(
            "insert into user_sign (id, user_id, time, sign)values(?,?,?,?)",
            (
                str(uuid.uuid4()),
                user_id,
                datetime.datetime.now().strftime("%Y-%m-%d"),
                str(random_circle_coordinates)
            )
        )
    bg = await draw_bg()
    for index in range(len(random_circle_coordinates) - 1):
        if index != 0 and random_circle_coordinates[index + 1] == (500, 500):
            continue
        bg = draw_line_between_points(bg, random_circle_coordinates[index], random_circle_coordinates[index + 1])
    # 最后在bg上居中位置且靠底部的位置写字
    bg = write_char(user_name, bg)
    save = f"{ABSOLUTE_PATH}\\cache\\{user_id}.jpg"
    bg.save(save)
    return save
    