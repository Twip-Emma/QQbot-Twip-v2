'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-10-07 10:53:46
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-10-07 20:09:26
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