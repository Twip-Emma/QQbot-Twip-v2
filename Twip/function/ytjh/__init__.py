'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-03-27 09:01:10
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-09-03 22:59:02
FilePath: \060坎公骑冠剑会战工具\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import re
from pathlib import Path
import httpx
from PIL import Image

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from tool.find_power.format_data import is_level_A
from tool.QsPilUtils2.dao import text_to_image

from Twip import SUPERUSERS

BASE_PATH: str = Path(__file__).absolute().parents[0]
CONFIG_PATH: str = Path(BASE_PATH) / "config.json"
pattern = re.compile(r"url=(.*?)&amp;")

__plugin_meta__ = PluginMetadata(
    name='云图攻略',
    description='提供《云图计划》各种攻略表的查询',
    usage='''云图算法/云图强度/云图印记/云图帮助''',
    extra={'version': 'v1.0.0',
           'cost': '无消耗'}
)


get_sf = on_command("云图算法", aliases={"云图算法表", "云图算法榜"}, block=True, priority=1)
get_qd = on_command("云图强度", aliases={
                  "云图强度表", "云图强度榜", "云图节奏", "云图节奏表", "云图节奏榜"}, block=True, priority=1)
get_yj = on_command("云图印记", aliases={"云图印记表", "云图印记榜"}, block=True, priority=1)
get_help = on_command(
    "云图帮助", aliases={"云图帮助表", "帮助云图", "云图 帮助"}, block=True, priority=1)

# 管理员指令
set_sf = on_command("云图设置算法", block=True, priority=1)
set_yj = on_command("云图设置印记", block=True, priority=1)
set_qd = on_command("云图设置强度", block=True, priority=1)
get_key = on_command("云图查看配置文件", block=True, priority=1)
reset_key = on_command("云图重置配置文件", block=True, priority=1)


@get_sf.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    try:
        await get_sf.send(MessageSegment.image(f"file:///{get_resp_img(json.load(open(CONFIG_PATH, 'r', encoding='utf8'))['sf'])}"))
    except:
        await get_sf.send("该命令下没有配置图片，请联系管理员！")

@get_yj.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    try:
        await get_yj.send(MessageSegment.image(f"file:///{get_resp_img(json.load(open(CONFIG_PATH, 'r', encoding='utf8'))['yj'])}"))
    except:
        await get_yj.send("该命令下没有配置图片，请联系管理员！")


@get_qd.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    try:
        await get_qd.send(MessageSegment.image(f"file:///{get_resp_img(json.load(open(CONFIG_PATH, 'r', encoding='utf8'))['qd'])}"))
    except:
        await get_qd.send("该命令下没有配置图片，请联系管理员！")


@get_help.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    message = """
    云图计划-帮助
    可支持的指令有：
        云图算法  查看算法推荐表
        云图强度  查看角色强度榜
        云图印记  查看印记推荐
        云图设置算法 <key:String> <value:Image>
        云图设置印记 <key:String> <value:Image>
        云图设置强度 <key:String> <value:Image>
        云图查看配置文件
        云图重置配置文件 <key:String|None>
    """
    await get_help.send(MessageSegment.image(f"file:///{text_to_image(message,15,(20,20))}"))


@set_sf.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 校验
    try:
        check_data(event=event)
    except RuntimeError as e:
        await set_sf.send(e)

    # 图片
    message = str(event.get_message())
    match = pattern.search(message)
    if not match:
        raise RuntimeError("找不到图片，参数详情请发送[云图帮助]查看")
    url = match.group(1)

    # key值
    key = str(event.get_message()).split()[1]

    # 下载并存储图片
    print(url)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            file_path = Path(BASE_PATH) / "cache" / f"{key}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
    except RuntimeError as e:
        await set_sf.send(e)

    # 同步配置文件
    json_config: dict = json.load(open(CONFIG_PATH, 'r', encoding='utf8'))
    if key not in json_config["sf"]:
        json_config["sf"].append(key)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_config, ensure_ascii=False))
            f.close()

    await set_sf.send("设置成功")


@set_yj.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 校验
    try:
        check_data(event=event)
    except RuntimeError as e:
        await set_yj.send(e)

    # 图片
    message = str(event.get_message())
    match = pattern.search(message)
    if not match:
        raise RuntimeError("找不到图片，参数详情请发送[云图帮助]查看")
    url = match.group(1)

    # key值
    key = str(event.get_message()).split()[1]

    # 下载并存储图片
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            file_path = Path(BASE_PATH) / "cache" / f"{key}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
    except RuntimeError as e:
        await set_yj.send(e)

    # 同步配置文件
    json_config: dict = json.load(open(CONFIG_PATH, 'r', encoding='utf8'))
    if key not in json_config["sf"]:
        json_config["yj"].append(key)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_config, ensure_ascii=False))
            f.close()

    await set_yj.send("设置成功")


@set_qd.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 校验
    try:
        check_data(event=event)
    except RuntimeError as e:
        await set_qd.send(e)

    # 图片
    message = str(event.get_message())
    match = pattern.search(message)
    if not match:
        raise RuntimeError("找不到图片，参数详情请发送[云图帮助]查看")
    url = match.group(1)

    # key值
    key = str(event.get_message()).split()[1]

    # 下载并存储图片
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            file_path = Path(BASE_PATH) / "cache" / f"{key}.jpg"
            with open(file_path, "wb") as f:
                f.write(response.content)
    except RuntimeError as e:
        await set_qd.send(e)

    # 同步配置文件
    json_config: dict = json.load(open(CONFIG_PATH, 'r', encoding='utf8'))
    if key not in json_config["sf"]:
        json_config["qd"].append(key)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_config, ensure_ascii=False))
            f.close()

    await set_qd.send("设置成功")


@get_key.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 权限
    if event.user_id not in SUPERUSERS:
        await get_key.send("权限不足")
    
    json_config: dict = json.load(open(CONFIG_PATH, 'r', encoding='utf8'))
    await get_key.send(MessageSegment.image(f"file:///{text_to_image(str(json_config),15,(20,20))}"))


@reset_key.handle()
@is_level_A
async def _(bot: Bot, event: GroupMessageEvent, cost=0):
    # 权限
    if event.user_id not in SUPERUSERS:
        await reset_key.send("权限不足")
    
    json_config: dict = json.load(open(CONFIG_PATH, 'r', encoding='utf8'))

    key = None
    i = len(str(event.get_message()).split())
    if i == 1:
        key = None
    else:
        key = str(event.get_message()).split()[1]

    try:
        if key:
            json_config[key] = []
        else:
            json_config = {"sf": [], "qd": [], "yj": []}
    except:
        await reset_key.send(f"配置文件找不到 {key} 这个key，请发送[云图查看键值对]查看")

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_config, ensure_ascii=False))
            f.close()

    await reset_key.send("设置成功")
    

# 校验合法性
def check_data(event: GroupMessageEvent) -> None:
    # 权限
    if event.user_id not in SUPERUSERS:
        raise RuntimeError("权限不足")

    # 参数
    if len(str(event.get_message()).split()) != 3:
        raise RuntimeError("参数不对，请发送[云图帮助]查看")


# 合成大图
def get_resp_img(image_paths:list) -> str:
    # 用于存储图片的路径列表
    for index in range(0, len(image_paths)):
        image_paths[index] = f"{BASE_PATH}\\cache\\{image_paths[index]}.jpg"

    print(image_paths)

    # 打开并加载所有图片
    images = [Image.open(path) for path in image_paths]
    

    # 获取每张图片的宽度和高度
    widths, heights = zip(*(i.size for i in images))

    # 计算拼接后的大图的宽度和高度
    max_width = max(widths)
    total_height = sum(heights)

    # 创建一个空白的大图
    result_image = Image.new("RGB", (max_width, total_height))

    # 将每张图片粘贴到大图上
    y_offset = 0
    for img in images:
        result_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    # 保存拼接后的大图到本地
    result_image.save(Path(BASE_PATH) / "cache" / "resp.jpg")
    return str(Path(BASE_PATH) / "cache" / "resp.jpg")






