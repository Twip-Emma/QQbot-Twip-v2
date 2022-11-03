'''
Author: 七画一只妖
Date: 2022-03-14 22:37:35
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-11-03 20:55:24
Description: file content
'''
import base64
from io import BytesIO

from tool.find_power.format_data import is_level_S
from os import path
import urllib.request
import requests

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

from PIL import Image
THIS_PATH = path.join(path.dirname(__file__))


BASE_URL = "https://pixiv.re/"


def get_image_from_url(pid: str) -> None:
    # image_url = f"{BASE_URL}{pid}.png"
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive',
               'Host': '<calculated when request is sent>',
               'User-Agent': 'PostmanRuntime/7.29.0'}
    resp = requests.get(url=BASE_URL + pid + ".png")
    print("==============================")
    print(resp)
    print("==============================")

    if resp.status_code != 200:
        return False

    filename = THIS_PATH + "\\image\\user_pixiv.png"
    with open(filename, 'wb') as f:
        f.write(resp.content)
    return True
    # image = Image.open(BytesIO(resp.content))


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


# 根据url获取图片
def get_image_from_url2(url: str) -> Image.Image:
    resp = requests.get(url=url, allow_redirects=False)
    image = Image.open(BytesIO(resp.content))
    return image


# 主控函数
def start(pid: str):
    # 获取图片
    return get_image_from_url(pid)
    # image = download_img(pid)
    # 判断图片是否有效
    # try:
    #     base64_str = img_to_b64(image)
    #     # 发送图片
    #     return base64_str
    # except:
    #     return None


get_pic = on_command("搜索图片", block=True, priority=2)


@get_pic.handle()
@is_level_S
async def _(bot: Bot, event: GroupMessageEvent, cost = 30):
    pid = event.message.extract_plain_text().split(" ")[1]
    re = start(pid)
    if re:
        await get_pic.send(MessageSegment.image("file:///" + THIS_PATH + "\\image\\user_pixiv.png"))
    else:
        await get_pic.send(f"获取失败，该作品下面可能有多张图片，请在pid后面连接第几张\n比如搜索pid为xxx的第2张：xxx-2")
        # await get_pic.send(MessageSegment.image(f"{BASE_URL}{pid}.png",proxy=False))


def download_img(pid: str):
    # header = {"Authorization": "Bearer " + api_token} # 设置http header
    print("就绪》》》》》")
    img_url = BASE_URL + pid + ".png"

    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        img_name = pid + ".png"
        filename = THIS_PATH + "\\image\\" + img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                print("开始下载》》》》》")
                f.write(response.read())  # 将内容写入图片
            return filename
    except:
        return "failed"

# if __name__ == '__main__':
#     # 下载要的图片
#     img_url = "http://www.baidu.com/some_img_url"
#     api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
#     download_img(img_url, api_token)
