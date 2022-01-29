import os, traceback, random, base64
from time import strftime, localtime, time, mktime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from datetime import datetime
# from nonebot import NoneBot
from io import BytesIO
from typing import Optional, Union
import nonebot

# from hoshino.config import SUPERUSERS
from nonebot.adapters.onebot.v11 import MessageSegment
# from hoshino.log import new_logger

from .api import *
from .sql import asql

arc = os.path.dirname(__file__)
songdir = os.path.join(arc, 'img', 'songs')
ver_json = os.path.join(arc, 'version.json')

diffdict = {
    '0' : ['pst', 'past'],
    '1' : ['prs', 'present'],
    '2' : ['ftr', 'future'],
    '3' : ['byd', 'beyond']
}

# log = new_logger('Arcaea_draw')

class Data:
    
    _img = os.path.join(arc, 'img')
    _recent_dir = os.path.join(_img, 'recent')
    _diff_dir = os.path.join(_img, 'diff')
    _song_dir = os.path.join(_img, 'songs')
    _rank_dir = os.path.join(_img, 'rank')
    _font_dir = os.path.join(_img, 'font')
    _char_dir = os.path.join(_img, 'char')
    _ptt_dir = os.path.join(_img, 'ptt')

    Exo_Regular = os.path.join(_font_dir, 'Exo-Regular.ttf')
    Kazesawa_Regular = os.path.join(_font_dir, 'Kazesawa-Regular.ttf')

    def __init__(self, project: str, info: dict) -> None:

        if project == 'recent':
            _playinfo = info['recent_score'][0]
            self.arcname: str = info['name']
            self.ptt: int = info['rating']
            self.character: int = info['character']
            self.is_char_uncapped: bool = info['is_char_uncapped']
            self.is_char_uncapped_override: bool = info['is_char_uncapped_override']
            self.songid: str = _playinfo['song_id']
            self.difficulty: int = _playinfo['difficulty']
            self.score: int = _playinfo['score']
            self.sp_count: int = _playinfo['shiny_perfect_count']
            self.p_count: int = _playinfo['perfect_count']
            self.far_count: int = _playinfo['near_count']
            self.miss_count: int = _playinfo['miss_count']
            self.health: int = _playinfo['health']
            self.play_time: int = _playinfo['time_played']
            self.rating: float = _playinfo['rating']

        elif project == 'best30':
            _playinfo = info[0]['data']
            self.scorelist: list = info[1:]
            self.arcname: str = _playinfo['name']
            self.character: int = _playinfo['character']
            self.is_char_uncapped: bool = _playinfo['is_char_uncapped']
            self.is_char_uncapped_override: bool = _playinfo['is_char_uncapped_override']
            self.ptt: int = _playinfo['rating']

        elif project == 'random':
            self._song_img = os.path.join(self._song_dir, info['song_id'], 'base.jpg' if info['difficulty'] != 3 else '3.jpg')
        else:
            raise TypeError
        
    async def recent(self) -> None:

        self._song_img = os.path.join(self._song_dir, self.songid, 'base.jpg' if self.difficulty != 3 else '3.jpg')
        _rank_img = os.path.join(self._rank_dir, f'grade_{self.isrank(self.score) if self.health != -1 else "F"}.png')
        _ptt_img = os.path.join(self._ptt_dir, self.pttbg(self.ptt))
        _bg_img = os.path.join(self._recent_dir, 'bg.png')
        _diff_img = os.path.join(self._recent_dir, f'{self.diff(self.difficulty)}.png')
        _black_line = os.path.join(self._recent_dir, 'black_line.png')
        _white_line = os.path.join(self._recent_dir, 'white_line.png')
        _time_img = os.path.join(self._recent_dir, 'time.png')
        
        character_name = f'{self.character}u_icon.png' if self.is_char_uncapped ^ self.is_char_uncapped_override else f'{self.character}_icon.png'
        _character_img = os.path.join(self._char_dir, character_name)

        self.song_img = await self.async_img(self._song_img, 'songs', self.songid, self.difficulty)
        c_img = await self.async_img(_character_img, 'char', character_name)
        self.character_img = c_img.resize((200, 200))
        self.rank_img = self.open_img(_rank_img)
        self.ptt_img = self.open_img(_ptt_img)
        self.bg_img = self.open_img(_bg_img)
        self.diff_img = self.open_img(_diff_img)
        self.black_line = self.open_img(_black_line)
        self.white_line = self.open_img(_white_line)
        self.time_img = self.open_img(_time_img)

    async def best30(self) -> None:

        _bg_img = os.path.join(self._img, 'b30_bg.png')
        _ptt_img = os.path.join(self._ptt_dir, self.pttbg(self.ptt))
        _black_line = os.path.join(self._img, 'black_line.png')
        _time_img = os.path.join(self._img, 'time.png')
        character_name = f'{self.character}u_icon.png' if self.is_char_uncapped ^ self.is_char_uncapped_override else f'{self.character}_icon.png'
        _character_img = os.path.join(self._char_dir, character_name)

        c_img = await self.async_img(_character_img, 'char', character_name)
        self.character_img = c_img.resize((250, 250))
        self.bg_img = self.open_img(_bg_img)
        self.ptt_img = self.open_img(_ptt_img).resize((150, 150))
        self.black_line = self.open_img(_black_line)
        self.time_img = self.open_img(_time_img)

    async def songdata(self, info: dict) -> None:

        self.songid: str = info['song_id']
        self.difficulty: int = info['difficulty']
        self.song_rating: float = info['constant']
        self.score: int = info['score']
        self.sp_count: int = info['shiny_perfect_count']
        self.p_count: int = info['perfect_count']
        self.far_count: int = info['near_count']
        self.miss_count: int = info['miss_count']
        self.health: int = info['health']
        self.play_time: int = info['time_played']
        self.rating: float = info['rating']

        _b30_img = os.path.join(self._img, 'b30_score_bg.png')
        _rank_img = os.path.join(self._rank_dir, f'grade_{self.isrank(self.score) if self.health != -1 else "F"}.png')
        _song_img = os.path.join(self._song_dir, self.songid, 'base.jpg' if self.difficulty != 3 else '3.jpg')
        _diff_img = os.path.join(self._diff_dir, f'{self.diff(self.difficulty).upper()}.png')
        _new_img = os.path.join(self._img, 'new.png')

        s_img = await self.async_img(_song_img, 'songs', self.songid, self.difficulty)
        self.song_img = s_img.resize((175, 175))
        self.b30_img = self.open_img(_b30_img)
        self.rank_img = self.open_img(_rank_img).resize((70, 40))
        self.diff_img = self.open_img(_diff_img)
        self.new_img = self.open_img(_new_img)

    def open_img(self, img: str) -> Image.Image:
        with open(img, 'rb') as f:
            im = Image.open(f).convert('RGBA')
        return im

    async def async_img(self, img: str, project: str, data: str, diff: int = None) -> Image.Image:
        if os.path.isfile(img):
            with open(img, 'rb') as f:
                im = Image.open(f).convert('RGBA')
            return im
        else:
            if diff:
                name = 'base.jpg' if diff != 3 else '3.jpg'
                new_img = await download_img(project, data, name)
            else:
                new_img = await download_img(project, data)
            if new_img:
                return self.open_img(img)

    @staticmethod
    def pttbg(ptt: int) -> str:
        if ptt == -1:
            return 'rating_off.png'
        ptt /= 100
        if ptt < 3:
            name = 'rating_0.png'
        elif ptt < 7:
            name = 'rating_1.png'
        elif ptt < 10:
            name = 'rating_2.png'
        elif  ptt < 11:
            name = 'rating_3.png'
        elif  ptt < 12:
            name = 'rating_4.png'
        elif  ptt < 12.5:
            name = 'rating_5.png'
        else:
            name = 'rating_6.png'
        return name

    @staticmethod
    def isrank(score: int) -> str:
        if score < 86e5:
            rank = 'd'
        elif score < 89e5:
            rank = 'c'
        elif score < 92e5:
            rank = 'b'
        elif score < 95e5:
            rank = 'a'
        elif score < 98e5:
            rank = 'aa'
        elif score < 99e5:
            rank = 'ex'
        else:
            rank = 'ex+'
        return rank

    @staticmethod
    def diff(difficulty: int) -> str:
        if difficulty == 0:
            diff = 'pst'
        elif difficulty == 1:
            diff = 'prs'
        elif difficulty == 2:
            diff = 'ftr'
        else:
            diff = 'byd'
        return diff

    @staticmethod
    def draw_fillet(img: Image.Image, radii: int, position: str = 'all') -> Image.Image:

        circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
        # 原图
        img = img.convert("RGBA")
        w, h = img.size
        alpha = Image.new('L', img.size, 255)
        if position == 'all':
            left_top = (0, 0, radii, radii)
            right_top = (radii, 0, radii * 2, radii)
            right_down = (radii, radii, radii * 2, radii * 2)
            left_down = (0, radii, radii, radii * 2)
        elif position == 'lt':
            left_top = (0, 0, radii, radii)
            right_top = (0, 0, 0, 0)
            right_down = (0, 0, 0, 0)
            left_down = (0, 0, 0, 0)
        elif position == 'rt':
            left_top = (0, 0, 0, 0)
            right_top = (radii, 0, radii * 2, radii)
            right_down = (0, 0, 0, 0)
            left_down = (0, 0, 0, 0)
        elif position == 'rd':
            left_top = (0, 0, 0, 0)
            right_top = (0, 0, 0, 0)
            right_down = (radii, radii, radii * 2, radii * 2)
            left_down = (0, 0, 0, 0)
        elif position == 'ld':
            left_top = (0, 0, 0, 0)
            right_top = (0, 0, 0, 0)
            right_down = (0, 0, 0, 0)
            left_down = (0, radii, radii, radii * 2)
        else:
            raise TypeError

        # 画4个角（将整圆分离为4个部分）
        alpha = Image.new('L', img.size, 255)
        alpha.paste(circle.crop(left_top), (0, 0))  # 左上角
        alpha.paste(circle.crop(right_top), (w - radii, 0))  # 右上角
        alpha.paste(circle.crop(right_down), (w - radii, h - radii))  # 右下角
        alpha.paste(circle.crop(left_down), (0, h - radii))  # 左下角
        # 白色区域透明可见，黑色区域不可见
        img.putalpha(alpha)

        return img

    @staticmethod
    def playtime(date: int) -> str:
        timearray = localtime(date / 1000)
        datetime = strftime('%Y-%m-%d %H:%M:%S', timearray)
        return datetime

    @property
    def songbg(self) -> str:
        return self._song_img

    @property
    def song_bg_img(self) -> Image.Image:
        bg_w, bg_h = self.song_img.size
        fix_w, fix_h = [1200, 900]

        scale = fix_w / bg_w
        w = int(scale * bg_w)
        h = int(scale * bg_h)

        re = self.song_img.resize((w, h))
        crop_height = (h - fix_h) / 2

        crop_img = re.crop((0, crop_height, w, h - crop_height))

        bg_gb = crop_img.filter(ImageFilter.GaussianBlur(3))
        bg_bn = ImageEnhance.Brightness(bg_gb).enhance(2 / 4.0)

        return bg_bn

class DrawText:

    def __init__(self, 
                image: Image.Image,
                X: float,
                Y: float,
                size: int,
                text: str,
                font: str,
                color: tuple = (255, 255, 255, 255),
                stroke_width: int = 0,
                stroke_fill: tuple = (0, 0, 0, 0),
                anchor: str = 'lt') -> None:
        self._img = image
        self._pos = (X, Y)
        self._text = str(text)
        self._font = ImageFont.truetype(font, size)
        self._color = color
        self._stroke_width = stroke_width
        self._stroke_fill = stroke_fill
        self._anchor = anchor

    def draw_text(self) -> Image.Image:

        text_img = Image.new('RGBA', self._img.size, (255, 255, 255, 0))
        draw_img = ImageDraw.Draw(text_img)
        draw_img.text(self._pos, self._text, self._color, self._font, self._anchor, stroke_width=self._stroke_width, stroke_fill=self._stroke_fill)
        return Image.alpha_composite(self._img, text_img)

def calc_rating(project: int, songrating: Optional[float] = 0, score: Optional[int] = 0, rating: Optional[float] = 0) -> Union[int, float]:
    if project == 0:
        '''用定数和分数算ptt'''
        if score >= 1e7:
            result = songrating + 2
        elif score >= 98e5:
            result = songrating + 1 + (score - 98e5) / 2e5
        else:
            result = songrating + (score - 95e5) / 3e5
    elif project == 1:
        '''用定数和ptt算分数'''
        if rating - 2 == songrating:
            result = 1e7
        elif rating - 2 < songrating and rating >= songrating:
            result = 98e5 + (rating - songrating - 1) * 2e5
        elif rating < songrating:
            result = 95e5 + (rating - songrating) * 3e5
    elif project == 2:
        '''用分数和ptt算定数'''
        if score >= 1e7:
            result = rating - 2
        elif score >= 98e5:
            result = rating - 1 - (score - 98e5) / 2e5
        else:
            result = rating - (score - 95e5) / 3e5
        result = float(f'{result:.1f}')
    
    return result

def timediff(date: int) -> float:
    now = mktime(datetime.now().timetuple())
    time_diff = (now - date / 1000) / 86400
    return time_diff

def img2b64(img: Image.Image) -> str:
    bytesio = BytesIO()
    img.save(bytesio, 'PNG')
    bytes = bytesio.getvalue()
    base64_str = base64.b64encode(bytes).decode()
    return 'base64://' + base64_str

async def draw_info(arcid: int) -> str:
    try:
        best30sum = 0
        print(f'Start Arcaea API {Data.playtime(time() * 1000)}')
        info = await arcb30(arcid)
        print(f'End Arcaea API {Data.playtime(time() * 1000)}')
        if not isinstance(info, list):
            return info
        data = Data('best30', info)

        await data.best30()
        
        data.scorelist.sort(key = lambda v: v['data'][0]['rating'], reverse=True)
        for i in range(30) if len(data.scorelist) >= 30 else range(len(data.scorelist)):
            best30sum += data.scorelist[i]['data'][0]['rating']
        
        ptt = data.ptt / 100 if data.ptt != -1 else '--'
        b30 = best30sum / 30
        r10 = (ptt - b30 * 0.75) / 0.25
        # 底图
        im = Image.new('RGBA', (1800, 3000))
        im.alpha_composite(data.bg_img)
        # 搭档
        im.alpha_composite(data.character_img, (175, 255))
        # ptt背景
        im.alpha_composite(data.ptt_img, (300, 380))
        # ptt
        im = DrawText(im, 375, 455, 45, f'{ptt:.2f}', data.Exo_Regular, anchor='mm', stroke_width=1, stroke_fill=(0, 0, 0, 255)).draw_text()
        # arcname
        im = DrawText(im, 455, 380, 85, data.arcname, data.Exo_Regular, anchor='lb').draw_text()
        # arcid
        im = DrawText(im, 480, 455, 60, f'ID:{arcid}', data.Exo_Regular, anchor='lb').draw_text()
        # r10
        im = DrawText(im, 1100, 380, 60, f'Recent 10: {r10:.3f}', data.Exo_Regular, anchor='lb').draw_text()
        # b30
        im = DrawText(im, 1100, 405, 60, f'Best 30: {b30:.3f}', data.Exo_Regular).draw_text()
        # 30个成绩
        bg_y = 540
        for num, i in enumerate(data.scorelist):
            if num == 30:
                break
            # 横3竖10
            if num % 3 == 0:
                bg_y += 245 if num != 0 else 0
                bg_x = 20
            else:
                bg_x += 590

            await data.songdata(i['data'][0])

            # 背景
            im.alpha_composite(data.b30_img, (bg_x + 40, bg_y))
            # 难度
            im.alpha_composite(data.diff_img, (bg_x + 40, bg_y + 25))
            # 曲绘
            im.alpha_composite(data.song_img, (bg_x + 70, bg_y + 50))
            # rank
            rank_xy = (bg_x + 425, bg_y + 120) if data.health != -1 else (bg_x + 450, bg_y + 135)
            im.alpha_composite(data.rank_img, rank_xy)
            # 黑线
            im.alpha_composite(data.black_line, (bg_x + 70, bg_y + 48))
            # 时间
            im.alpha_composite(data.time_img, (bg_x + 245, bg_y + 205))

            songinfo = asql.song_info(data.songid, data.diff(data.difficulty))
            title = songinfo[1] if songinfo[1] else songinfo[0]

            im = DrawText(im, bg_x + 290, bg_y + 35, 20, title, data.Kazesawa_Regular, (0, 0, 0, 255), anchor='mm').draw_text()
            # songrating
            if data.song_rating < 10:
                sr = f'{data.song_rating:.1f}'
                im = DrawText(im, bg_x + 55, bg_y + 110, 20, sr[0], data.Exo_Regular, anchor='mm').draw_text()
                im = DrawText(im, bg_x + 55, bg_y + 120, 20, sr[1], data.Exo_Regular, anchor='mm').draw_text()
                im = DrawText(im, bg_x + 55, bg_y + 140, 20, sr[2], data.Exo_Regular, anchor='mm').draw_text()
            else:
                sr = f'{data.song_rating:.1f}'
                im = DrawText(im, bg_x + 55, bg_y + 100, 20, sr[0], data.Exo_Regular, anchor='mm').draw_text()
                im = DrawText(im, bg_x + 55, bg_y + 120, 20, sr[1], data.Exo_Regular, anchor='mm').draw_text()
                im = DrawText(im, bg_x + 55, bg_y + 130, 20, sr[2], data.Exo_Regular, anchor='mm').draw_text()
                im = DrawText(im, bg_x + 55, bg_y + 150, 20, sr[3], data.Exo_Regular, anchor='mm').draw_text()
            # 名次
            im = DrawText(im, bg_x + 530, bg_y + 35, 45, num + 1, data.Exo_Regular, (0, 0, 0, 255), anchor='mm').draw_text()
            # 分数
            im = DrawText(im, bg_x + 260, bg_y + 75, 45, f'{data.score:,}', data.Exo_Regular, (0, 0, 0, 255), anchor='lm').draw_text()
            # PURE 
            im = DrawText(im, bg_x + 260, bg_y + 130, 30, 'P', data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            im = DrawText(im, bg_x + 290, bg_y + 130, 25, data.p_count, data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            im = DrawText(im, bg_x + 355, bg_y + 130, 20, f'| +{data.sp_count}', data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            # FAR
            im = DrawText(im, bg_x + 260, bg_y + 162, 30, 'F', data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            im = DrawText(im, bg_x + 290, bg_y + 162, 25, data.far_count, data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            # LOST
            im = DrawText(im, bg_x + 260, bg_y + 194, 30, 'L', data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            im = DrawText(im, bg_x + 290, bg_y + 194, 25, data.miss_count, data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            # Rating
            im = DrawText(im, bg_x + 360, bg_y + 194, 25, f'Rating | {data.rating:.2f}', data.Exo_Regular, (0, 0, 0, 255), anchor='ls').draw_text()
            # time
            im = DrawText(im, bg_x + 395, bg_y + 215, 20, data.playtime(data.play_time), data.Exo_Regular, anchor='mm').draw_text()
            # # new
            if timediff(data.play_time) <= 7:
                im.alpha_composite(data.new_img, (bg_x + 32, bg_y - 8))
        # save
        base64str = img2b64(im)
        msg = MessageSegment.image(base64str)
    except Exception as e:
        print(traceback.print_exc())
        msg = f'Error {type(e)}'
    return msg

async def draw_score(user_id: int, est: bool = False) -> Union[MessageSegment, str]:
    try:
        # 获取用户名
        if est:
            scoreinfo = await arcb30(user_id, est)
            if isinstance(scoreinfo, str):
                return scoreinfo
            userinfo = scoreinfo['data']
            arcid = user_id
        else:
            arcid, email, pwd = asql.get_bind_user(user_id)
            scoreinfo = await get_web_api(email, pwd)
            if isinstance(scoreinfo, str):
                return scoreinfo
            friends = scoreinfo['value']['friends']
            for n, i in enumerate(friends):
                if user_id == i['user_id']:
                    userinfo = friends[n]
                    break
                
        data = Data('recent', userinfo)
        await data.recent()

        ptt = data.ptt / 100 if data.ptt != -1 else '--'
        # 歌曲信息
        songinfo = asql.song_info(data.songid, data.diff(data.difficulty))
        title = songinfo[1] if songinfo[1] else songinfo[0]
        if songinfo[3] == -1:
            if data.rating > 0:
                songrating = calc_rating(2, score=data.score, rating=data.rating)
                asql.add_song_rating(data.songid, data.diff(data.difficulty), songrating * 10)
            else:
                songrating = -1
        else:
            songrating = songinfo[3] / 10

        diffi = data.diff(data.difficulty)
        im = Image.new('RGBA', (1200, 900))
        # 底图
        im.alpha_composite(data.song_bg_img)
        # 白线
        im.alpha_composite(data.white_line, (140, 132))
        # 搭档
        im.alpha_composite(data.character_img, (500, 35))
        # ptt背景
        im.alpha_composite(data.ptt_img, (585, 140))
        # 成绩背景
        im.alpha_composite(data.bg_img, (50, 268))
        # 黑线
        im.alpha_composite(data.black_line, (50, 333))
        # 曲绘
        song_img_fillet = data.draw_fillet(data.song_img, 25, 'ld')
        im.alpha_composite(song_img_fillet, (50, 338))
        # 难度
        im.alpha_composite(data.diff_img, (50, 800))
        # 时间
        im.alpha_composite(data.time_img, (562, 800))
        # 评价
        im.alpha_composite(data.rank_img, (900, 630) if data.health != -1 else (950, 650))
        # 昵称
        im = DrawText(im, 290, 100, 50, data.arcname, data.Exo_Regular, anchor='mm').draw_text()
        # 好友码
        im = DrawText(im, 290, 170, 40, arcid, data.Exo_Regular, anchor='mm').draw_text()
        # ptt
        im = DrawText(im, 644, 197, 40, ptt, data.Exo_Regular, stroke_width=1, stroke_fill=(0, 0, 0, 255), anchor='mm').draw_text()
        # rating
        im = DrawText(im, 750, 135, 60, f'Rating: {data.rating:.2f}', data.Exo_Regular, anchor='lm').draw_text()
        # 曲名
        im = DrawText(im, 600, 300, 45, title, data.Kazesawa_Regular, color=(0, 0, 0, 255), anchor='mm').draw_text()
        # 分数
        im = DrawText(im, 600, 410, 100, f'{data.score:,}', data.Exo_Regular, color=(0, 0, 0, 255), anchor='lm').draw_text()
        # Pure
        im = DrawText(im, 600, 550, 55, 'Pure', data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Player Pure
        im = DrawText(im, 800, 550, 55, f'{data.p_count} (+{data.sp_count})', data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Far
        im = DrawText(im, 600, 635, 55, 'Far', data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Player Far
        im = DrawText(im, 800, 635, 55, data.far_count, data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Lost
        im = DrawText(im, 600, 720, 55, 'Lost', data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Player Lost
        im = DrawText(im, 800, 720, 55, data.miss_count, data.Exo_Regular, color=(0, 0, 0, 255), anchor='ls').draw_text()
        # Difficulty
        im = DrawText(im, 306, 825, 40, f'{diffi.upper()} | {songrating}', data.Exo_Regular, anchor='mm').draw_text()
        # Time
        im = DrawText(im, 858, 825, 40, data.playtime(data.play_time), data.Exo_Regular, anchor='mm').draw_text()

        base64str = img2b64(im)
        msg = MessageSegment.image(base64str)
        
    except Exception as e:
        print(traceback.print_exc())
        msg = f'Error {type(e)}'
    return msg

def random_music(rating: int, plus: bool, diff: int) -> str:

    difficulty = 0
    if diff:
        difficulty = diff
        song = asql.get_song(rating, plus, diffdict[str(diff)][0])
    elif plus:
        song = asql.get_song(rating, plus)
    else:
        song = asql.get_song(rating)

    if rating % 10 != 0 and diff:
        for i in song:
            if i[diff + 4] != rating:
                song.remove(i)

    if not song:
        return '未找到符合的曲目'

    random_list_int = random.randint(0, len(song) - 1)
    songinfo = song[random_list_int]

    songrating = [str(i / 10) for n, i in enumerate(songinfo) if n >= 4 and i != -1]
    diffc = [diffdict[str(_)][0].upper() for _ in range(len(songrating))]

    songs = {
        'song_id': songinfo[0],
        'difficulty': difficulty
    }

    data = Data('random', songs)

    msg = f'''[CQ:image,file=file:///{data.songbg}]
Song: {songinfo[2] if songinfo[2] else songinfo[1]}
Artist: {songinfo[3]}
Difficulty: {' | '.join(diffc)}
Rating: {' | '.join(songrating)}'''

    return msg

def bindinfo(qqid: int, arcid: int, arcname: str, gid: int) -> str:
    asql.insert_temp_user(qqid, arcid, arcname.lower(), gid)
    return f'用户 {arcid} 已成功绑定QQ {qqid}，现可使用 <arcinfo> 指令查询B30成绩和 <arcre:> 指令使用 est 查分器查询最近，<arcre> 指令需等待管理员确认是否为好友才能使用，确认添加为好友后BOT将会在绑定的群@您提醒账号已绑定'

async def newbind() -> None:
    try:
        bind_id, email, password = asql.get_not_full_email()
        info = await get_web_api(email, password)
        if isinstance(info, str):
            return info
        friend = info['value']['friends']
        for m in friend:
            arcname = m['name']
            user_id = m['user_id']
            name = asql.get_user_name(user_id)
            if name: continue
            asql.insert_user(arcname.lower(), user_id, bind_id)
            user = asql.get_gid(user_id)
            if not user:
                await nonebot.get_bot().send_private_msg(user_id=1157529280, message=f'玩家：{arcname} 添加失败，可能游戏名错误')
                continue
            await nonebot.get_bot().send_group_msg(group_id=user[1], message=f'{MessageSegment.at(user[0])} 您的arc账号已绑定成功，现可用所有arc指令')
            asql.delete_temp_user(user[0])
            print(f'玩家：<{arcname}> 添加成功')
        return '添加成功'
    except Exception as e:
        print(f'Error：{traceback.print_exc()}')
        await nonebot.get_bot().send_private_msg(user_id=1157529280, message=f'添加失败：{e}')
        return '添加失败'
