'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-07 10:53:46
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-17 12:01:44
FilePath: \060坎公骑冠剑会战工具\payload2\test2.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
from PIL import Image, ImageDraw, ImageFont
import warnings
from pathlib import Path
warnings.filterwarnings("ignore",category=DeprecationWarning)

BASE_PATH: str = Path(__file__).absolute().parents[0]

# 测试颜色字典
COLOR_LIST = {
    "侵略者导演": (123,123,0),
    "熔岩史莱姆国王": (0,123,123),
    "海军舰长玛丽娜": (200,123,0),
    "归来的收割者": (15,123,26),
}

# 测试数据
TEAT_DATA = {
    "Aus周逗": {
        "侵略者导演": 16015127,
        "熔岩史莱姆国王": 51938873,
        "海军舰长玛丽娜": 40362454,
        "归来的收割者": 15776083
    },
    "槐诗": {
        "熔岩史莱姆国王": 2597834,
        "侵略者导演": 26832165,
        "归来的收割者": 15776083
    },
    "江城月哉": {
        "侵略者导演": 31233118
    },
    "糖吉诃德": {
        "海军舰长玛丽娜": 9145931
    },
    "khk": {
        "侵略者导演": 32389012,
        "海军舰长玛丽娜": 25734366
    }
}


# 获取柱状图图表
def make_image(data, user_id):

    # 获取所有怪物种类
    monsters = set(monster for user_data in data.values() for monster in user_data.keys())

    # 为每种怪物分配随机颜色
    color_dict = {}
    for monster in monsters:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color_dict[monster] = color

    # 用户数据打印
    font_size = 15
    
    # 按照总伤害大小对用户进行排序
    sorted_users = sorted(data.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # 计算总用户数和最大伤害值
    usernames = [user[0] for user in sorted_users]
    monsters = list(set(monster for user_data in data.values() for monster in user_data.keys()))

    total_max_damage = max([sum(user_data.values()) for user_data in data.values()])
    image_width = min(total_max_damage / total_max_damage * 1000, 1000) + 200  # 加上左右边距
    image_height = (len(usernames) + 1) * (20 + 20) + 50

    image = Image.new('RGB', (int(image_width), int(image_height)), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # font = ImageFont.load_default()
    from pathlib import Path
    BASE_PATH: str = Path(__file__).absolute().parents[0]
    font = ImageFont.truetype(f"{BASE_PATH}\\a.ttf", font_size)

    #######################图例#######################
    # 计算图例的宽度和高度
    legend_width = 1000
    legend_height = 50

    # 计算图例的位置
    image_width = min(total_max_damage / total_max_damage * 1000, 1000) + 200
    image_height = (len(usernames) + 1) * (20 + 20) + 50 + legend_height  # 增加图例的高度
    # legend_x = (image_width - legend_width) / 2  # 水平居中
    legend_y = image_height - legend_height  # 放在图表下方

    # 创建包含图例的新图像
    legend_image = Image.new('RGB', (legend_width, legend_height), (255, 255, 255))
    legend_draw = ImageDraw.Draw(legend_image)
    legend_font = ImageFont.truetype(f"{BASE_PATH}\\a.ttf", )

    # 绘制图例
    legend_x_offset = 125
    for monster, color in color_dict.items():
        legend_draw.rectangle([(10 + legend_x_offset, 10), (30+ legend_x_offset, 10 + 10)], fill=color)
        legend_draw.text((40+ legend_x_offset, 10), monster, fill=(0, 0, 0), font=legend_font)
        legend_x_offset += 250

    # 创建主图像
    image = Image.new('RGB', (int(image_width), int(image_height)), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(f"{BASE_PATH}\\a.ttf", )


    #######################柱状图#######################
    # 绘制柱状图
    y = 50

    for username, user_data in sorted_users:
        total_damage = sum(user_data.values())
        x = 100  # 左边距宽度
        y_end = y + 20
        draw.text((10, y + 10), username, fill=(0, 0, 0), font=font)
        for monster in monsters:
            damage = user_data.get(monster, 0)
            bar_length = (damage / total_max_damage) * (image_width - 200)  # 减去左边距宽度
            color = color_dict.get(monster, (255, 0, 0))
            draw.rectangle([(x, y), (x + bar_length, y_end)], fill=color)
            
            # 在柱子内显示伤害，以万为单位，仅当伤害大于0时显示
            if damage > 0:
                damage_text = str(int(damage / 10000))
                text_width, _ = draw.textsize(damage_text, font=font)
                text_x = x + bar_length / 2 - text_width / 2
                text_y = y + 5  # 调整纵向位置
                draw.text((text_x, text_y), damage_text, fill=(0, 0, 0), font=font)
            
            x += bar_length
        
        # 在柱子后面展示总伤害数字，以万为单位，仅当总伤害大于0时显示
        if total_damage > 0:
            total_damage_text = str(int(total_damage / 10000))
            # total_damage_width, _ = draw.textsize(total_damage_text, font=font)
            total_damage_x = x + 10  # 距离最后一个柱子的右边距宽度
            total_damage_y = y + 5  # 调整纵向位置
            draw.text((total_damage_x, total_damage_y), total_damage_text, fill=(0, 0, 0), font=font)
        
        y += 40

    # 合并主图像和图例
    image.paste(legend_image, (0, int(legend_y)))

    # 保存图表为图片文件
    # image.show()
    path = f"{BASE_PATH}\\cache\\表格图_{user_id}.jpg"
    image.save(path)
    return path


# 合成进度表
def get_rate_image(text:str, user_id:str) -> str:
    # 将文本转图片
    font = ImageFont.truetype(f"{BASE_PATH}\\a.ttf", )
    image = Image.new("RGB", (270, 180), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))
    path = f"{BASE_PATH}\\cache\\进度表_{user_id}.jpg"
    image.save(path)
    return path



# 合成出刀表
def get_knife_image(data: dict, user_id: str, date_list:list) -> str:
    # 定义表格的大小和格子的高度
    table_width = 8
    table_height = 31
    cell_height = 50

    # 计算表格的宽度
    cell_widths = [300] + [50] * (table_width - 1)
    table_width_px = sum(cell_widths)

    # 计算表格的高度
    table_height_px = table_height * cell_height

    # 定义边缘距离
    margin = 30

    # 创建图像，考虑边缘距离
    img_width = table_width_px + 2 * margin
    img_height = table_height_px + 2 * margin
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)

    # 绘制表格线条，考虑边缘距离
    line_width = 2
    x = margin

    # 绘制纵向线条
    for width in cell_widths:
        draw.line([(x, margin), (x, img_height - margin)],
                  fill='black', width=line_width)
        x += width

    # 补上最后一列右侧的线条
    draw.line([(x, margin), (x, img_height - margin)],
              fill='black', width=line_width)

    # 绘制横向线条
    y = margin
    for i in range(table_height + 1):
        draw.line([(margin, y), (img_width - margin, y)],
                  fill='black', width=line_width)
        y += cell_height

    # 在第一行的每个格子中写上数字 1 到 7，确保居中
    font_size = 25
    font = ImageFont.truetype(f"{BASE_PATH}\\a.ttf", font_size)

    for col in range(1, table_width):
        number = str(col)
        text_width, text_height = draw.textsize(number, font=font)

        # 计算居中位置
        x_centered = margin + \
            sum(cell_widths[1:col + 1]) - cell_widths[col] + \
            (cell_widths[col] - text_width) // 2
        y_centered = margin + (cell_height - text_height) // 2

        # 在图像上绘制文本
        draw.text((x_centered + 300, y_centered),
                  number, fill='black', font=font)

    # 在表格中填入数据，从第二行开始
    for row, (name, date_data) in enumerate(data.items(), start=1):
        # 在第一列写入成员名字，确保居中
        text_width, text_height = draw.textsize(name, font=font)
        x_centered = margin + (cell_widths[0] - text_width) // 2
        y_centered = margin + row * cell_height + \
            (cell_height - text_height) // 2
        draw.text((x_centered, y_centered), name, fill='black', font=font)
        index = 1
        for col, number in enumerate(range(1, table_width), start=1):
            try:
                date = date_list[len(date_list) - index - 1]
            except:
                date = "不存在的日期"
            value = date_data.get(date, 0)  # 如果日期数据不存在，填充为0
            value_str = str(value)
            text_width, text_height = draw.textsize(value_str, font=font)

            # 计算居中位置
            x_centered = margin + \
                sum(cell_widths[1:col + 1]) - cell_widths[col] + \
                (cell_widths[col] - text_width) // 2
            y_centered = margin + row * cell_height + \
                (cell_height - text_height) // 2

            # 检查数值是否为3，如果不是则填充红色
            text_color = 'red' if value != 3 else 'black'

            # 在图像上绘制文本
            draw.text((x_centered + 300, y_centered),
                      value_str, fill=text_color, font=font)
            index += 1
    path = f"{BASE_PATH}\\cache\\出刀图_{user_id}.jpg"
    img.save(path)
    return path
