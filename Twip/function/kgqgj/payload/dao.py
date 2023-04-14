'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 10:45:06
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-04-14 22:58:51
'''
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import datetime

from .function import f_get_damage_data, f_get_rate_data, f_get_dao_total, f_get_dao_daily, f_get_damage_total
from .utils.image_utils import write_longsh, FontEntity
from .utils.data_utils import data_format
from .setting import FIGHT_LIST

BASE_PATH: str = Path(__file__).absolute().parents[0]
FONT_PATH = f"{BASE_PATH}\\ttf\\yuanshen.ttf"


# 获取当日出刀表图
async def get_data(date: str = None):
    """
    获取指定日期的出刀图，如果为空则为当日的出刀
    注意:在会战日期之外必须传日期
    date:日期（xxxx-xx-xx）
    返回:图片路径
    """

    if date is None:
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.datetime.strptime(now, "%Y-%m-%d").date()
        latest_time = datetime.datetime.strptime(FIGHT_LIST[-1], "%Y-%m-%d").date()
        date = now if latest_time > now_time else latest_time


    d_data: dict = await f_get_damage_data(date)

    # 数据整合（生成排版文字）
    text1 = f"""===今日数据（{date}，第1-10名）===\n\n"""
    text2 = f"""===今日数据（{date}，第11-20名）===\n\n"""
    text3 = f"""===今日数据（{date}，第21-30名）===\n\n"""
    d_data = data_format(d_data)
    for index, item in enumerate(sorted(d_data, key=lambda i: i["damage_total"], reverse=True), 1):
        fight_total = sum([1 if d_tiem["is_kill"] == 1 else 2 for d_tiem in item["damage_list"]])
        fight_total = min(fight_total, 6) * 0.5
        if fight_total in [0, 1, 2, 3]:
            fight_total = int(fight_total)
        if index <= 10:
            text1 += f"""{index}.{item["user_name"]}({fight_total}/3) 总伤害：{item["damage_total"]}\n"""
            for d_tiem in item["damage_list"]:
                text1 += f""">     {d_tiem["boss_name"]:>5}   {d_tiem["damage"]}\n"""
            text1 += ">\n"
        elif 11 <= index <= 20:
            text2 += f"""{index}.{item["user_name"]}({fight_total}/3) 总伤害：{item["damage_total"]}\n"""
            for d_tiem in item["damage_list"]:
                text2 += f""">     {d_tiem["boss_name"]:>5}   {d_tiem["damage"]}\n"""
            text2 += ">\n"
        elif 21 <= index <= 30:
            text3 += f"""{index}.{item["user_name"]}({fight_total}/3) 总伤害：{item["damage_total"]}\n"""
            for d_tiem in item["damage_list"]:
                text3 += f""">     {d_tiem["boss_name"]:>5}   {d_tiem["damage"]}\n"""
            text3 += ">\n"
        else:
            break

    # 图像处理
    FONTSIZE = 18
    font = FontEntity(fsize=FONTSIZE, ttf_path=FONT_PATH)

    bg = Image.new("RGB", (1500, 1500), (255, 255, 255))
    image = write_longsh(font_entity=font, img=bg, text=text1, dis=(50, 50), mode="L")
    image2 = write_longsh(font_entity=font, img=image, text=text2, dis=(500, 50), mode="L")
    image3 = write_longsh(font_entity=font, img=image2, text=text3, dis=(950, 50), mode="L")
    save_path = f"{BASE_PATH}\\cache\\daily_damage.jpg"
    with open(save_path, "wb") as f:
        image3.save(f)
    return save_path



# 获取伤害总榜以及出刀数
async def get_data_total():
    """
    获取伤害总榜以及出刀数，手动修改setting.py的日期list
    注意:在会战日期之外必须传日期
    date:日期（xxxx-xx-xx）
    返回:图片路径
    """

    # 获取数据并排序
    total_data: dict = {}
    for date in FIGHT_LIST:
        date: dict = await f_get_damage_data(date)
        for item in date:
            # 先遍历有效出刀数
            fight_total = 0
            for d_tiem in item["damage_list"]:
                if d_tiem["is_kill"] == 1:
                    fight_total += 1
                else:
                    fight_total += 2
            if fight_total > 6:
                fight_total = 6
            # 计入数据
            if item["user_name"] not in total_data.keys():
                total_data.update(
                    {item["user_name"]: {
                        "damage_total": item["damage_total"],
                        "fight_total": fight_total
                    }}
                )
            else:
                total_data[item["user_name"]
                           ]["damage_total"] += item["damage_total"]
                total_data[item["user_name"]]["fight_total"] += fight_total

    total_data = sorted(total_data.items(),
                        key=lambda i: i[1]["damage_total"], reverse=True)

    # 输出图片
    text = "===总伤害排行===\n\n\n"
    index = 1
    for item in total_data:
        text += f"第{index}名（{item[1]['fight_total']}/84）：{item[0]:<10}  {item[1]['damage_total']:<10}\n\n"
        index += 1
    # 图像处理
    fsize = 20
    font = FontEntity(fsize=fsize, ttf_path=FONT_PATH)

    # 计算高度
    line, max_text = _get_max_size(text)
    dis = (50, 50)

    _f = ImageFont.truetype(FONT_PATH, 20)
    width, _ = _f.getsize(max_text)

    page_height = int((dis[0] * 2 + fsize * line) * 1.1)
    page_width = int((dis[1] * 2 + width) * 1.1)

    text.split("#")
    bg = Image.new("RGB", (page_width, page_height), (255, 255, 255))
    image = write_longsh(font_entity=font, img=bg,
                         text=text, dis=dis, mode="L")
    save_path = f"{BASE_PATH}\\cache\\total_damage.jpg"
    image.save(save_path)
    return save_path


# 获取文本行数和最长字符串个数
def _get_max_size(text: str) -> tuple:
    """
    获取文本行数和最长字符串
    text:文本
    返回:(文本行数，最长字符串)
    """
    _text = text.split("\n")
    line = len(_text)

    max_line = 0
    max_text = ""
    for item in _text:
        this_line = len(item)
        if max_line < this_line:
            max_text = item
            max_line = this_line
    return line, max_text


async def get_rate():
    resp_data: dict = await f_get_rate_data()

    image_size = (550, 170)
    font = ImageFont.truetype(FONT_PATH, size=15)

    # Create image and drawing object
    image = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Define table headers
    headers = ['BOSS名称', '等级', '属性', '总血量', '当前血量', "百分比"]

    # Define table data
    # data = [['九尾狐佳岚', '66', '光', '2640000', '2640000'],
    #         ['宰相邓肯', '66', '暗', '2640000', '2640000']]

    # 数据转换
    data: list = []
    for item in resp_data["boss"][-4:]:
        data_item = [str(item["name"]),
                     str(item["level"]),
                     item["elemental_type_cn"],
                     str(item["total_hp"]),
                     str(item["remain_hp"]),
                     _percentage(item["remain_hp"],item["total_hp"])]
        data.append(data_item)

    # Define column widths
    col_widths = [120, 40, 40, 120, 120, 40]

    # Draw table headers
    x_pos = 10
    y_pos = 10
    for i, header in enumerate(headers):
        draw.text((x_pos, y_pos), header, font=font, fill=(0, 0, 0))
        x_pos += col_widths[i]

    # Draw table data
    y_pos += 30
    for row in data:
        x_pos = 10
        for i, cell in enumerate(row):
            draw.text((x_pos, y_pos), cell, font=font, fill=(0, 0, 0))
            x_pos += col_widths[i]
        y_pos += 30

    # Save image as "rate.jpg" in the current working directory
    save_path = f"{BASE_PATH}\\cache\\rate.jpg"
    image.save(save_path)
    return save_path


async def get_dao_total_image():
    return await f_get_dao_total()


async def get_dao_daily_image():
    return await f_get_dao_daily()


async def get_dao_damage_total_image():
    return await f_get_damage_total()
    

def _percentage(smaller, bigger):
    if smaller == 0:
        return '0.00%'
    return '{:.2%}'.format(float(smaller) / float(bigger))
