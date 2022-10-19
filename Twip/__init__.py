'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-09 13:27:39
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-19 14:21:01
'''
from os import path
from pathlib import Path
from typing import List

from nonebot import get_driver, load_plugins, logger
from nonebot.plugin import PluginMetadata
from tool.utils.logger import logger as my_logger
from setting import *

DRIVER = get_driver()
__version__ = 'v2.0.0beta3-fix2'

try:
    SUPERUSERS: List[int] = [int(s) for s in DRIVER.config.superusers]
except KeyError:
    SUPERUSERS = []
    logger.error('请在.env.prod文件中中配置超级用户SUPERUSERS')

try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except KeyError:
    NICKNAME = 'Twip'

ABSOLUTE_PATH = path.join(path.dirname(__file__))


__plugin_meta__ = PluginMetadata(
    name='Twip',
    description='核心模块，为其他功能服务，守护模块',
    usage='''使用方式：无''',
    extra={'version': 'v2.0.0beta3-fix2',
           'cost': '###0'}
)


logo = """<g>
___________       .__        
\__    ___/_  _  _|__|_____  
  |    |  \ \/ \/ /  \____ \ 
  |    |   \     /|  |  |_> >
  |____|    \/\_/ |__|   __/ 
                     |__|    </g>"""



@DRIVER.on_startup
async def startup():
    logger.opt(colors=True).success(logo)
    my_logger.success('初始化', f'机器人昵称：<m>{NICKNAME}</m>')
    my_logger.success('初始化', f'超级管理员：<m>{SUPERUSERS}</m>')
    my_logger.success('初始化', f'成功加载绝对路径头：<m>{ABSOLUTE_PATH}</m>')
    my_logger.success('配置文件', f'开始验证配置文件是否生效')
    try:
        if URL == None or USER_CARD == None or PASS_WORD == None or DATABASE == None or Api_Key == None or Api_Secret == None or Content_Type == None:
            raise ImportError
    except:
        my_logger.warning("配置文件",f"配置不完整，请前往根目录，创建setting/__init__.py创建，详细内容请查阅Readme")
        my_logger.warning('警告', f'<m>配置不完整，可能会造成功能异常！！！</m>')
        return
    my_logger.success('配置文件', f'检查完成，机器人继续运行，<m>请自行保证参数的可用性！！！</m>')


@DRIVER.on_shutdown
async def shutdown():
    my_logger.warning('关闭', f'机器人<m>{NICKNAME}</m>已成功断开链接')


# 加载来自商店的模块
# load_plugins(str(Path(__file__).parent / 'plugins'))
# load_plugins("Twip/plugins")

# 加载自己写的模块
# load_plugins("Twip/admin")
load_plugins("Twip/function")
# load_plugins("Twip/user")
# load_plugins("Twip/listener")
# load_plugins("Twip/speaker")
# load_plugins("Twip/help")
