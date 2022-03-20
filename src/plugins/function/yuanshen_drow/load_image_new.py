'''
Author: 七画一只妖
Date: 2021-10-21 19:06:13
LastEditors: 七画一只妖
LastEditTime: 2022-03-20 16:31:05
Description: file content
'''
from PIL import Image, ImageFont, ImageDraw, ImageMath
from loguru import logger
from io import BytesIO


import httpx
import re
import os


# 同级
from .user_config import ICON_PATH, FILE_PATH


POOL_API = "https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/gacha/list.json"
ROLES_API = ['https://genshin.honeyhunterworld.com/db/char/characters/?lang=CHS',
             'https://genshin.honeyhunterworld.com/db/char/unreleased-and-upcoming-characters/?lang=CHS']
ARMS_API = ['https://genshin.honeyhunterworld.com/db/weapon/sword/?lang=CHS',
            'https://genshin.honeyhunterworld.com/db/weapon/claymore/?lang=CHS',
            'https://genshin.honeyhunterworld.com/db/weapon/polearm/?lang=CHS',
            'https://genshin.honeyhunterworld.com/db/weapon/bow/?lang=CHS',
            'https://genshin.honeyhunterworld.com/db/weapon/catalyst/?lang=CHS']
ROLES_HTML_LIST = None
ARMS_HTML_LIST = None
FONT_PATH = f"{os.path.dirname(__file__)}\\yuanshen.ttf"
FONT = ImageFont.truetype(FONT_PATH, size=20)


# 获取角色或武器的图标，直接返回 Image
async def get_icon(url):
    icon = await get_url_data(url)
    icon = Image.open(BytesIO(icon))
    icon_a = icon.getchannel("A")
    icon_a = ImageMath.eval("convert(a*b/256, 'L')", a=icon_a, b=icon_a)
    icon.putalpha(icon_a)
    return icon


# 获取角色属性，直接返回属性图标 Image
async def get_role_element(en_name):
    url = f'https://genshin.honeyhunterworld.com/db/char/{en_name}/?lang=CHS'
    data = await get_url_data(url)
    data = data.decode("utf-8")
    element = re.search('/img/icons/element/.+?_35.png', data).group()
    element = element[19:-7]

    element_path = os.path.join(FILE_PATH, 'icon', f'{element}.png')
    return Image.open(element_path)


# 获取url的数据
async def get_url_data(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url)
        if resp.status_code != 200:
            raise ValueError(f"从 {url} 获取数据失败，错误代码 {resp.status_code}")
        return resp.content


# 从 genshin.honeyhunterworld.com 获取角色的英文名
async def get_role_en_name(ch_name):
    global ROLES_HTML_LIST
    if ROLES_HTML_LIST == None:
        ROLES_HTML_LIST = []
        for api in ROLES_API:
            data = await get_url_data(api)
            ROLES_HTML_LIST.append(data.decode("utf-8"))
    pattern = ".{80}" + str(ch_name)
    for html in ROLES_HTML_LIST:
        txt = re.search(pattern, html)
        if txt == None:
            continue
        txt = re.search('"/db/char/.+/\?lang=CHS"', txt.group()).group()
        en_name = txt[10:-11]
        return en_name
    raise NameError(f"没有找到角色 {ch_name} 的图标名")


# 更新角色图标
async def up_role_icon(name, star):
    role_name_path = os.path.join(ICON_PATH, "角色图鉴", str(name) + ".png")
    if os.path.exists(role_name_path):
        return
    logger.info(f"正在更新 {name} 角色图标")
    if not os.path.exists(os.path.join(ICON_PATH, '角色图鉴')):
        os.makedirs(os.path.join(ICON_PATH, '角色图鉴'))
    role_icon = await paste_role_icon(name, star)
    with open(role_name_path, "wb") as icon_file:
        role_icon.save(icon_file)


# 获取指定角色的图片，并保存
async def paste_role_icon(ch_name ,star):
    en_name = await get_role_en_name(ch_name)
    url = f"https://genshin.honeyhunterworld.com/img/char/{en_name}_gacha_card.png"
    avatar_icon = await get_icon(url)
    return avatar_icon


# 更新武器图标
async def up_arm_icon(name, star):
    # 更新武器图标
    arm_name_path = os.path.join(ICON_PATH, "武器图鉴", str(name) + ".png")
    if os.path.exists(arm_name_path):
        return
    logger.info(f"正在更新 {name} 武器图标")
    if not os.path.exists(os.path.join(ICON_PATH, '武器图鉴')):
        os.makedirs(os.path.join(ICON_PATH, '武器图鉴'))

    arm_icon = await paste_arm_icon(name, star)
    with open(arm_name_path, "wb") as icon_file:
        arm_icon.save(icon_file)


# 获取武器图
async def paste_arm_icon(ch_name, star):
    # 拼接武器图鉴图
    arm_id = await get_arm_id(ch_name)
    url = f'https://genshin.honeyhunterworld.com/img/weapon/{arm_id}_gacha.png'
    arm_icon = await get_icon(url)
    return arm_icon


async def get_icon(url):
    # 获取角色或武器的图标，直接返回 Image
    icon = await get_url_data(url)
    icon = Image.open(BytesIO(icon))
    icon_a = icon.getchannel("A")
    icon_a = ImageMath.eval("convert(a*b/256, 'L')", a=icon_a, b=icon_a)
    icon.putalpha(icon_a)
    return icon


async def get_arm_id(ch_name):
    # 从 genshin.honeyhunterworld.com 获取武器的ID
    global ARMS_HTML_LIST
    if ARMS_HTML_LIST == None:
        ARMS_HTML_LIST = []
        for api in ARMS_API:
            data = await get_url_data(api)
            ARMS_HTML_LIST.append(data.decode("utf-8"))

    pattern = '.{40}' + str(ch_name)
    for html in ARMS_HTML_LIST:
        txt = re.search(pattern, html)
        if txt == None:
            continue
        txt = re.search('weapon/.+?/\?lang', txt.group()).group()
        arm_id = txt[7:-6]
        return arm_id
    raise NameError(f"没有找到武器 {ch_name} 的 ID")


###################################################################################
# 启用前初始化，初始化卡池数据
async def init_pool_list(char_info:dict) -> str:
    global ROLES_HTML_LIST
    ROLES_HTML_LIST = None

    print(char_info)
    if char_info["type"] == '角色':
        await up_role_icon(name=char_info["name"], star=char_info["star"])
    else:
        await up_arm_icon(name=char_info["name"], star=char_info["star"])

    # 根据类型返回路径
    if char_info["type"] == '角色':
        return os.path.join(ICON_PATH, '角色图鉴', char_info["name"] + '.png')
    else:
        return os.path.join(ICON_PATH, '武器图鉴', char_info["name"] + '.png')