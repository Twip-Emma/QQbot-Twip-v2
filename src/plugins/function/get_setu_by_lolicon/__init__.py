'''
Author: 七画一只妖
Date: 2022-04-14 18:06:48
LastEditors: 七画一只妖
LastEditTime: 2022-04-14 19:32:54
Description: file content
'''
from os import path
import requests
import json

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from tool.find_power.format_data import is_level_S

API_DEFULT = "https://api.lolicon.app/setu/v2"
THIS_PATH = path.join(path.dirname(__file__))


# NEW_URL = "https://api.pixiv.moe/image/i.pximg.net/img-master/img/2020/09/10/01/12/34/84270031_p0.jpg"
# "https://api.pixiv.moe/image/i.pximg.net/img-master/img/2018/12/23/12/59/57/72242348_p0_master1200.jpg"
# "https://api.pixiv.moe/image/i.pximg.net/img-master/img/2018/12/23/12/59/57/72242348_p0.jpg"
NEW_URL = "https://api.pixiv.moe/image/i.pximg.net/img-master"


get_setu = on_command("~购买涩图")


@get_setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        return
    group_id = event.group_id

    msg_list = []

    original, pid, tags = get_setu_url(API_DEFULT)
    img_path = download_img(original)

    # 判断文件大小是否小于100KB
    while path.getsize(img_path) <= 100:
        original, pid, tags = get_setu_url(API_DEFULT)
        img_path = download_img(original)

    message_list = [f"画作PID: {pid}", f"图片链接: {original}", f"图片大小: {path.getsize(img_path)}",f"画作标签：{tags}",f"[CQ:image,file=file:///{img_path}]"]

    for data_msg in message_list:
        data = {
            "type": "node",
            "data": {
                "name": "Twip的替身",
                "uin": "2854196310",
                "content": data_msg
            }
        }
        msg_list.append(data)
    await bot.send_group_forward_msg(group_id=group_id, messages=msg_list)


get_tags_setu = on_command("~标签涩图")


@get_tags_setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if not is_level_S(event):
        return
    try:
        group_id = event.group_id
        args = str(event.get_message()).split()

        tag_list_str = "?"
        if len(args) == 1:
            await bot.send_group_msg(group_id=group_id, message=f"在指令后面输入tag哦，以空格隔开")
            return
        else:
            for i in range(1,len(args)):
                tag_list_str += "tag=" + args[i] + "&"

        # 删除最后一个&
        tag_list_str = tag_list_str[:-1]

        new_url = API_DEFULT + tag_list_str

        msg_list = []

        original, pid, tags = get_setu_url(new_url)
        img_path = download_img(original)

        # 判断文件大小是否小于100KB
        while path.getsize(img_path) <= 100:
            original, pid, tags = get_setu_url(new_url)
            img_path = download_img(original)

        message_list = [f"画作PID: {pid}", f"图片链接: {original}", f"图片大小: {path.getsize(img_path)}",f"画作标签：{tags}",f"[CQ:image,file=file:///{img_path}]"]

        for data_msg in message_list:
            data = {
                "type": "node",
                "data": {
                    "name": "Twip的替身",
                    "uin": "2854196310",
                    "content": data_msg
                }
            }
            msg_list.append(data)
        await bot.send_group_forward_msg(group_id=group_id, messages=msg_list)
    except Exception as e:
        await bot.send_group_msg(group_id=group_id, message=f"出错了，请联系管理员，建议不要乱输标签\n{e}")


# 下载图片
def download_img(url: str) -> str:
    '''
    下载图片
    '''
    filename = THIS_PATH + "\\image\\user_pixiv.png"
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)
    return filename


# 获取图片链接
def get_setu_url(url:str):
    '''
    获取图片
    '''
    if url == "":
        url = API_DEFULT
    r = requests.get(url)
    r.encoding = "uft-8"
    a: dict = json.loads(r.text)
    original = a["data"][0]["urls"]["original"]
    original = original.replace("https://i.pixiv.cat/img-original","https://api.pixiv.moe/image/i.pximg.net/img-master")
    original = original.replace(".jpg","_master1200.jpg")
    original = original.replace(".png","_master1200.jpg")
    pid = a["data"][0]["pid"]
    tags = str(a["data"][0]["tags"])
    return original,pid,tags



# url = get_setu_url(API_DEFULT)
# print(download_img(url))