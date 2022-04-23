'''
Author: 七画一只妖
Date: 2022-04-22 21:53:24
LastEditors: 七画一只妖
LastEditTime: 2022-04-23 15:12:44
Description: file content
'''
from io import BytesIO
from os import path
from PIL import Image, ImageDraw, ImageFont
FILE_PATH = path.join(path.dirname(__file__))


# 将传入的文字转图片
async def text_to_pic(text: str) -> str:

    bg = Image.new("RGB", (650, 4000), (255, 255, 255))
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\zh-cn.ttf", 15)
    dr.text((10, 180), text=text, font=font, fill="#000000")


    title_text1 = f"一下曲目均来自七画一只妖在《冰与火之舞》这款游戏的收藏\n"
    title_text2 = f"注意，以下等级均为论坛等级与个人体感折中所得\n"
    title_text3 = f"等级计为21.1代表该铺面原本理论上人类无法一命完成\n"
    title_text4 = f"等级计为21.0代表该铺面原本理论上人类无法一命完成，却意外有高手击破了\n"
    
    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(f"{FILE_PATH}\\zh-cn.ttf", 17)
    # 将text3和text4居中
    text_width1 = font.getsize(text=title_text1)
    text_width2 = font.getsize(text=title_text2)
    text_width3 = font.getsize(text=title_text3)
    text_width4 = font.getsize(text=title_text4)
    text_width5 = font.getsize(text="By  Twip  七画一只妖")
    dr.text(((650-text_width1[0])/2,20), text=title_text1, font=font, fill="#000000")
    dr.text(((650-text_width2[0])/2,50), text=title_text2, font=font, fill="#000000")
    dr.text(((650-text_width3[0])/2,80), text=title_text3, font=font, fill="#000000")
    dr.text(((650-text_width4[0])/2,110), text=title_text4, font=font, fill="#000000")
    dr.text(((650-text_width5[0])/2,140), text="By  Twip  七画一只妖", font=font, fill="#000000")


    
    # 保存图片到\data内，命名为all_song.jpg
    bg.save(f"{FILE_PATH}\\data\\all_song.jpg")
    return f"{FILE_PATH}\\data\\all_song.jpg"