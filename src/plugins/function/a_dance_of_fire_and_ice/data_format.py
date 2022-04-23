'''
Author: 七画一只妖
Date: 2022-04-23 10:24:49
LastEditors: 七画一只妖
LastEditTime: 2022-04-23 12:56:34
Description: file content
'''
import os
import json

from .image_format import text_to_pic


# 加载绝对路径头
ABSOLUTE_PATH = os.path.join(os.path.dirname(__file__))


# 加载song_info.json
SONG_INFO = f"{ABSOLUTE_PATH}\\data\\song_info.json"


# 遍历song_info.json
async def get_song_info() -> bytes:
    with open(SONG_INFO, "r", encoding="utf-8") as f:
        song_info:dict = eval(f.read())

    # 遍历son_info变成一个列表
    song_info_list = []
    for key, value in song_info.items():
        song_info_list.append(value)

    # 根据level对song_info进行排序
    song_info_list.sort(key=lambda x: x["level"])

    # 遍历
    index = 1
    song_info_msg = ""
    for song in song_info_list:
        song_info_msg += f"{index}.{song['name']}(LEVEL {song['level']}) 来源：{song['address']} | 曲师：{song['author']} | 谱师：{song['mapby']}\n\n"
        index += 1
    
    return await text_to_pic(song_info_msg)


# 新增一个歌曲
async def add_song(name:str , level:str , address:str , author:str , mapby:str) -> str:

    # level保留一位小数转float
    level = float(level)

    song_info = { name :
        {"name": name,
        "level": level,
        "address": address,
        "author": author,
        "mapby": mapby}
    }

    data:dict = json.load(open(SONG_INFO, 'r', encoding='utf8'))

    data.update(song_info)

    with open(SONG_INFO, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()

    return "添加成功"


# 删除一个歌曲
async def del_song(name:str) -> str:
    
        data:dict = json.load(open(SONG_INFO, 'r', encoding='utf8'))

        # 判断是否存在
        if name in data:
            del data[name]
    
            with open(SONG_INFO, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.close()
        
            return "删除成功"
        else:
            return "删除失败，你输入的曲目名称不存在"