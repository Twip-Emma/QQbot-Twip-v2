'''
Author: 七画一只妖
Date: 2022-03-14 22:37:35
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-31 10:34:04
Description: file content
'''
import os
import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from pathlib import Path
BASE_PATH: str = Path(__file__).absolute().parents[0]
from tool.find_power.format_data import is_level_S

IMAGE_FOLDER = f"{BASE_PATH}\\cache"

BASE_URL = "https://pixiv.re"

__plugin_meta__ = PluginMetadata(
    name='P站插画搜索',
    description='查询P站插画',
    usage='''搜索图片 <插画pid>''',
    extra={'version': 'v1.0.0',
           'cost': '30'}
)

get_pic = on_command("搜索图片", block=True, priority=2)


@get_pic.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost = 30):
    pid = event.message.extract_plain_text().split(" ")[1]
    img_url = f"{BASE_URL}/{pid}.png"
    
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    downloaded_image_path = await download_image(img_url, IMAGE_FOLDER)

    if downloaded_image_path:
        await get_pic.send(MessageSegment.image(f"file:///{downloaded_image_path}"))
    else:
        await get_pic.send("下载失败，请检查日志！")


async def download_image(img_url, save_folder):
    # 获取图片文件名
    img_name = img_url.split("/")[-1]
    
    # 拼接保存路径
    save_path = os.path.join(save_folder, img_name)
    print(save_path)
    
    async with httpx.AsyncClient() as client:
        # 发起HTTP请求并下载图片
        response = await client.get(img_url, follow_redirects=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return save_path
        else:
            print("Failed to download image.")
            return None