'''
Author: 七画一只妖
Date: 2022-01-23 17:22:57
LastEditors: 七画一只妖
LastEditTime: 2022-01-23 17:34:51
Description: file content
'''
import aiohttp, websockets, json, brotli, os
from typing import Union
# from hoshino.log import new_logger

from .sql import asql

api = 'https://webapi.lowiro.com/'
me = 'webapi/user/me'
login = 'auth/login'
est = 'wss://arc.estertion.win:616/'

imgapi = 'http://106.53.138.218:6321/api/'
char_api = 'arcaea/char/'

dir = os.path.join(os.path.dirname(__file__), 'img')
# logger = new_logger('Arcaea')

async def get_web_api(email: str, password: str) -> Union[str, dict]:
    data = {'email': email, 'password': password}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api + login, data=data) as req:
                if req.status != 200:
                    return '查询用账号异常，请联系BOT管理员'
            async with session.get(api + me) as reqs:
                return await reqs.json()
    except Exception as e:
        return f'Error {type(e)}'


async def arcb30(arcid: str, re: bool = False) -> Union[str, dict]:
    try:
        b30_data = []
        async with websockets.connect(est, timeout=10) as ws:
            await ws.send(str(arcid))
            while True:
                if ws.closed:
                    break
                data = await ws.recv()
                if data == 'error,add':
                    return '连接查分器错误'
                elif data == 'error,Please update arcaea':
                    return '查分器未更新游戏版本'
                elif data == 'error,invalid user code':
                    return '好友码无效'
                elif data == 'bye':
                    return b30_data
                elif isinstance(data, bytes):
                    info = json.loads(brotli.decompress(data))
                    if info['cmd'] == 'userinfo' and re:
                        return info
                    elif info['cmd'] == 'scores' or info['cmd'] == 'userinfo':
                        b30_data.append(info)
    except websockets.ConnectionClosedError as e:
        return '可能在排队，请暂时停用<arcinfo>和<arcre:>指令'
    except Exception as e:
        return f'Error: {type(e)}'

async def download_img(project: str, data: str, name: int = None):
    if project == 'songs':
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{imgapi}arcaea?songid={data}') as req:
                new_data = await req.json()
        
        songid = new_data['songid']
        artist = new_data['artist']
        name_en = new_data['name_en']
        name_jp = new_data['name_jp']
        if name == 'base.jpg':
            url = new_data['base_url']
        else:
            url = new_data['byd_url'] if 'byd_url' in new_data else ''
        result = asql.song_info(songid, 'ftr')
        if not result:
            asql.add_song(songid, name_en, name_jp, artist)

        new_dir = os.path.join(dir, 'songs', data)
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)
        dirname = os.path.join(new_dir, name)
    elif project == 'char':
        url = imgapi + char_api + data
        dirname = os.path.join(dir, 'char', data)
    if os.path.isfile(dirname):
        return False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                data = await req.read()
                open(dirname, 'wb').write(data)
                print(f'文件：{dirname} 下载完成')
                return True
    except Exception as e:
        print(f'文件：{dirname} 下载失败')
        return f'Error {type(e)}'