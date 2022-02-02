'''
Author: 七画一只妖
Date: 2022-02-01 19:51:00
LastEditors: 七画一只妖
LastEditTime: 2022-02-02 15:19:51
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, MessageSegment
import nonebot

import requests
import os
import random
import base64
import time
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from tool.find_power.format_data import is_level_S

my_friend_say = on_command('我朋友说')
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-cn"
           }

fontpath = os.path.join(os.path.dirname(__file__), 'msyh.ttc')
head_path = os.path.join(os.path.dirname(__file__), '1.png')
body_path = os.path.join(os.path.dirname(__file__), '2.png')
end_path = os.path.join(os.path.dirname(__file__), '3.png')

# tlmt = hoshino.util.DailyNumberLimiter(10)

# def check_lmt(uid): #次数限制
#     flmt_g = hoshino.util.FreqLimiter(0)
#     if uid in hoshino.config.SUPERUSERS:
#         return 0, ''
#     if not tlmt.check(uid):
#         return 1, "您今天已经呼叫过10次朋友了,朋友累了,请明天再来!"
#     tlmt.increase(uid,1)
#     return 0, ''


async def member_list_load(bot, gid):
    _list = await nonebot.get_bot().get_group_member_list(group_id=gid)
    return _list


class IDloader:
    def __init__(self, bot, ev, member_list, mode=1):
        self.group_id = ev.group_id
        self.member_list = member_list
        self.owner_id = self.get_group_owener_id()
        self.admin_list = self.get_group_admin_id()
        self.active_member_list = self.get_group_member_id()
        self.at_qq, self.at_name = self.load_at(ev)
        if mode == 1:
            self.text = self.load_text_prefix(ev)
        elif mode == 2:
            self.text = self.load_text_match(ev)

    def get_group_owener_id(self):  # 获取群主qq
        for member in self.member_list:
            if member["role"] == "owner":
                return member['user_id']
        else:
            return None

    def get_group_admin_id(self):  # 获取管理qq
        member_list = []
        for member in self.member_list:
            if member['role'] == 'admin':
                member_list.append(member['user_id'])
        return member_list

    def get_group_member_id(self):  # 获取qq号列表，排除掉长时间（大约30天）不活跃的群友
        member_list = []
        now = time.time()
        for member in self.member_list:
            if now - member['last_sent_time'] < 2500000:
                member_list.append(member)
        return member_list

    def choice_random_member(self, sex=''):  # 根据性别随机获得群员qq
        temp = []
        for member in self.active_member_list:
            # print(self.active_member_list)
            if sex == '' or sex == member['sex'] or member['sex'] == 'unknown':
                temp.append(member['user_id'])
        return random.choice(temp)

    def load_at(self, ev):  # 从消息中提取at信息
        try:
            for msg in ev.message:
                if msg.type == 'at':
                    uid = int(msg.data['qq'])
                    for member in self.member_list:
                        if member['user_id'] == uid:
                            name = member['card'] if member['card'] else member['nickname']
                            break
                    return uid, name
            else:
                return None, None
        except Exception as e:
            print(repr(e))
            return None, None

    def load_text_match(self, ev):
        match = ev.match
        self.name = str.strip(ev['match'].group(1))
        if not self.at_qq:
            for member in self.member_list:
                if (member['card'] and member['card'] == self.name) or member['nickname'] == self.name:
                    self.at_qq = member['user_id']
        return str.strip(ev['match'].group(2))

    def load_text_prefix(self, ev):
        return ev.message.extract_plain_text().strip()


async def request_img(uid):
    response = requests.get(
        f' http://q1.qlogo.cn/g?b=qq&nk={uid}&s=100', headers=headers)
    image = Image.open(BytesIO(response.content))
    image = image.resize((125, 125), Image.ANTIALIAS)
    return image


def strQ2B(c):  # 全角全部强制转半角（懒得处理全角符号的长度了）
    _c = ord(c)
    if _c == 12288:
        _c = 32
    elif 65281 <= _c <= 65374:
        _c -= 65248
    return chr(_c)


def remake_text(text):  # 对文本重新分行
    temp = ''
    len_ = 0
    text_list = []
    for i in text:
        if i == '\n':
            text_list.append(temp)
            len_ = 0
            temp = ''
            continue
        else:
            i = strQ2B(i)
            temp += i
        if '\u4e00' <= i <= '\u9fff':
            len_ += 50
        else:
            len_ += 26
        if len_ >= 611:
            text_list.append(temp)
            len_ = 0
            temp = ''
    if temp != '':
        text_list.append(temp)
    return text_list


async def make_pic(uid, text, name):
    padding = [230, 120]
    font = ImageFont.truetype(fontpath, 48)
    font_name = ImageFont.truetype(fontpath, 42)

    head = Image.open(head_path)
    draw = ImageDraw.Draw(head)
    draw.text((220, 18), name, font=font_name, fill=(123, 128, 140))

    body = Image.open(body_path)
    end = Image.open(end_path)

    text_list = remake_text(text)
    icon = await request_img(uid)

    wa = head.size[0]
    ha = 205 + len(text_list) * 53

    i = Image.new('RGB', (wa, ha), color=(255, 255, 255))
    i.paste(icon, (40, 27))
    if len(text_list) == 1:
        i.paste(end, (0, ha-end.size[1]))
        i.paste(head, (0, 0), head)
    else:
        body = body.resize((wa, ha-head.size[1]-end.size[1]), Image.ANTIALIAS)
        i.paste(head, (0, 0), head)
        i.paste(body, (0, head.size[1]))
        i.paste(end, (0, head.size[1]+body.size[1]))
    draw = ImageDraw.Draw(i)
    for j in range(len(text_list)):
        text = text_list[j]
        draw.text((padding[0], padding[1] + 53 * j),
                  text, font=font, fill=(0, 0, 0))

    msg1 = img_to_b64(i)
    # buf1 = BytesIO()
    # i.save(buf1, format='PNG')
    # base64_str1 = f'base64://{base64.b64encode(buf1.getvalue()).decode()}'
    # msg1 = f'''[CQ:image,file={base64_str1}]'''

    return msg1


# 转B64对象
def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


def sex_get(text):
    sex = ''
    if text[0] == '他':  # 简单的识别一下朋友性别
        sex = 'male'
    elif text[0] == '她':
        sex = 'female'
    _text = ''
    for i in text:  # 谓词转换，不需要可以注释掉
        if i in ['他', '她']:
            _text += '我'
            continue
        elif i == '我':
            _text += '你'
            continue
        elif i == '你':
            _text += '他'
            continue
        else:
            _text += i

    return sex, _text


@my_friend_say.handle()
async def _(bot: Bot, ev: GroupMessageEvent):
    if not is_level_S(ev):
        await my_friend_say.finish()
    # user_id = ev.user_id
    # flag, msg = check_lmt(user_id)
    # if flag:
    #     await bot.send(ev, msg, at_sender = True)
    #     return
    member_list = await member_list_load(bot, ev.group_id)
    info = IDloader(bot, ev, member_list, 1)
    if info.text == '':
        return
    else:
        sex, text = sex_get(info.text)
        uid = info.at_qq if info.at_qq else info.choice_random_member(sex)

    group_id = str(ev.group_id)
    recall_user_info = await bot.get_group_member_info(group_id=group_id, user_id=uid)
    recall_user_name = recall_user_info['nickname']

    msg = str(ev.get_message()).split()
    if len(msg) <= 1:
        await my_friend_say.finish("我们直到那天也不知道你朋友说了什么")
    text = msg[1]

    msg = await make_pic(uid, text, recall_user_name)
    await my_friend_say.finish(MessageSegment.image(msg))

# @sv.on_rex(r'^(.*)酱说(.*)')
# async def group_owner_say(bot, ev):
#     user_id = ev.user_id
#     flag, msg = check_lmt(user_id)
#     if flag:
#         await bot.send(ev, msg, at_sender = True)
#         return
#     member_list = await member_list_load(bot,ev.group_id)
#     info = IDloader(bot, ev, member_list, 2)
#     name = info.name if info.name else info.at_name
#     text = info.text
#     if text == '':
#         return
#     else:
#         sex, text = sex_get(text)
#     if info.at_qq:
#         uid = info.at_qq
#     elif name == '群主':
#         uid = info.owner_id
#     elif name == '管理':
#         uid = random.choice(info.admin_list)
#     else:
#         uid = info.choice_random_member(sex)
#     msg = await make_pic(uid,text,name)
#     await bot.send(ev, msg)
