'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-09 13:27:39
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-09 13:39:35
FilePath: \QQbot-Twip-v2\Twip\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from os import path
from pathlib import Path

from nonebot import load_plugins, get_driver, logger
from typing import List

from tool.utils.logger import logger as my_logger

DRIVER = get_driver()
__version__ = '2.0.0beta2'

try:
    SUPERUSERS: List[int] = [int(s) for s in DRIVER.config.superusers]
except KeyError:
    SUPERUSERS = []
    logger.error('请在.env.prod文件中中配置超级用户SUPERUSERS')

try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except KeyError:
    NICKNAME = '派蒙'

ABSOLUTE_PATH = path.join(path.dirname(__file__))

logo = """<g>
___________       .__        
\__    ___/_  _  _|__|_____  
  |    |  \ \/ \/ /  \____ \ 
  |    |   \     /|  |  |_> >
  |____|    \/\_/ |__|   __/ 
                     |__|    </g>"""


@DRIVER.on_startup
async def startup():
    logger.opt(colors=True).info(logo)
    my_logger.info('初始化', f'成功加载绝对路径头：<m>{ABSOLUTE_PATH}</m>')


# 加载来自商店的模块
load_plugins(str(Path(__file__).parent / 'plugins'))
load_plugins("Twip/admin")
load_plugins("Twip/function")
load_plugins("Twip/user")
load_plugins("Twip/listener")
load_plugins("Twip/speaker")
load_plugins("Twip/help")