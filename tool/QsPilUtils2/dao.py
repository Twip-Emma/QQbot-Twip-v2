'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-04-21 13:46:12
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-17 16:47:19
FilePath: \QQbot-Twip-v2\tool\QsPilUtils2\dao.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]


from PIL import Image, ImageDraw, ImageFont

def text_to_image(text: str, font_size: int = 20, spacing: tuple = (0, 0)):
    # 设置字体、字号、行高
    font_path = f'{BASE_PATH}\\ttf\\zh-cn.ttf'
    font = ImageFont.truetype(font_path, font_size)
    line_spacing = font.getsize('A')[1] + 8  # 行高比字体高度多8个像素

    # 计算文本宽度和高度
    lines = text.strip().split('\n')
    width = max(font.getsize(line)[0] for line in lines) + spacing[0] * 2
    height = line_spacing * len(lines) + spacing[1] * 2

    # 创建空白的图片对象
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 在图片上绘制文本
    draw = ImageDraw.Draw(image)
    x, y = spacing[0], spacing[1]
    for line in lines:
        draw.text((x, y), line, font=font, fill=(0, 0, 0))
        y += line_spacing

    # 保存图片
    save_path = f'{BASE_PATH}\\cache\\long_text.jpg'
    image.save(save_path)
    return save_path
