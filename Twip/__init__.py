'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-09 13:27:39
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-09-03 22:42:07
'''
from pathlib import Path
from typing import List

from nonebot import get_driver, load_plugins, logger
from nonebot.plugin import PluginMetadata
from tool.utils.logger import logger as my_logger

DRIVER = get_driver()
__version__ = 'v2.0.0beta3-fix2'

__plugin_meta__ = PluginMetadata(
    name='Twip',
    description='核心模块，为其他功能服务，守护模块',
    usage='''使用方式：无''',
    extra={'version': 'v2.0.0beta3-fix2',
           'cost': '无消耗'}
)

logo = """<g>
___________       .__        
\__    ___/_  _  _|__|_____  
  |    |  \ \/ \/ /  \____ \ 
  |    |   \     /|  |  |_> >
  |____|    \/\_/ |__|   __/ 
                     |__|    </g>"""

# ========================全局变量配置中心========================

# 超级管理员
try:
    SUPERUSERS: List[int] = [int(s) for s in DRIVER.config.superusers]
except KeyError:
    SUPERUSERS = []
    logger.error('请在.env.prod文件中中配置超级用户SUPERUSERS')

# 机器人称呼
try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except KeyError:
    NICKNAME = 'Twip'

# 核心模块根目录
ABSOLUTE_PATH: str = Path(__file__).absolute().parents[0]

# 项目根目录
BASE_PATH: str = Path(__file__).absolute().parents[1]

# 数据库连接
DB_URL = DRIVER.config.dict().get("db_url", None)
DB_CARD = DRIVER.config.dict().get("db_card", None)
DB_PASS = DRIVER.config.dict().get("db_pass", None)
DB_LIB = DRIVER.config.dict().get("db_lib", None)

# 茉莉云
MLY_KEY = DRIVER.config.dict().get("mly_key", None)
MLY_SECRET = DRIVER.config.dict().get("mly_secret", None)

# 字体
TTF_PATH = f"{BASE_PATH}\\ttf\\zh-cn.ttf"


# ========================校验全局变量========================
@DRIVER.on_startup
async def startup():
    logger.opt(colors=True).success(logo)
    my_logger.success('初始化', f'机器人昵称：<m>{NICKNAME}</m>')
    my_logger.success('初始化', f'超级管理员：<m>{SUPERUSERS}</m>')
    my_logger.success('初始化', f'成功加载绝对路径头：<m>{ABSOLUTE_PATH}</m>')
    my_logger.success('配置文件', f'开始验证配置文件是否生效')
    # 数据库配置校验
    try:
        if not DB_URL or not DB_CARD or not DB_PASS or not DB_LIB:
            raise ImportError
    except:
        my_logger.warning(
            "配置文件", f"数据库参数配置不完整，请查阅README进行配置")
        my_logger.warning('警告', f'<m>配置不完整，可能会造成功能异常！！！</m>')
        return
    
    # 校验其它参数
    try:
        if not MLY_KEY or not MLY_SECRET:
            raise ImportError
    except:
        my_logger.warning(
            "配置文件", f"茉莉云参数配置不完整，请查阅README进行配置")
        my_logger.warning('警告', f'<m>配置不完整，可能会造成功能异常！！！</m>')
    
    # 校验其它参数
    try:
        if not SUPERUSERS or not NICKNAME:
            raise ImportError
    except:
        my_logger.warning(
            "配置文件", f"机器人信息参数配置不完整，请查阅README进行配置")
        my_logger.warning('警告', f'<m>配置不完整，可能会造成功能异常！！！</m>')
    
    my_logger.success('配置文件', f'检查完成，机器人继续运行，<m>请自行保证参数的可用性！！！</m>')


@DRIVER.on_shutdown
async def shutdown():
    my_logger.warning('关闭', f'机器人<m>{NICKNAME}</m>已成功断开链接')


# 加载来自商店的模块
# load_plugins(str(Path(__file__).parent / 'plugins'))
load_plugins("Twip/plugins")
# load_plugins("Twip/bean")

# 加载自己写的模块
load_plugins("Twip/admin")
load_plugins("Twip/function")
load_plugins("Twip/user")
load_plugins("Twip/listener")
load_plugins("Twip/speaker")
load_plugins("Twip/help")
