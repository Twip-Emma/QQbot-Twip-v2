'''
Author: 七画一只妖
Date: 2022-09-15 19:43:58
LastEditors: 七画一只妖
LastEditTime: 2022-09-17 13:27:45
Description: file content
'''
from pathlib import Path

from nonebot import load_plugins, get_driver, logger, load_plugin
from typing import List
from LittlePaimon import database
from LittlePaimon.utils.migration import migrate_database
from LittlePaimon.utils.tool import check_resource

DRIVER = get_driver()
__version__ = '2.0.0beta1'

try:
    SUPERUSERS: List[int] = [int(s) for s in DRIVER.config.superusers]
except KeyError:
    SUPERUSERS = []
    logger.error('请在.env.prod文件中中配置超级用户SUPERUSERS')

try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except KeyError:
    NICKNAME = '派蒙'

logo = """<g>
██╗     ██╗████████╗████████╗██╗     ███████╗  ██████╗  █████╗ ██╗███╗   ███╗ ██████╗ ███╗   ██╗
██║     ██║╚══██╔══╝╚══██╔══╝██║     ██╔════╝  ██╔══██╗██╔══██╗██║████╗ ████║██╔═══██╗████╗  ██║
██║     ██║   ██║      ██║   ██║     █████╗    ██████╔╝███████║██║██╔████╔██║██║   ██║██╔██╗ ██║
██║     ██║   ██║      ██║   ██║     ██╔══╝    ██╔═══╝ ██╔══██║██║██║╚██╔╝██║██║   ██║██║╚██╗██║
███████╗██║   ██║      ██║   ███████╗███████╗  ██║     ██║  ██║██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝</g>"""


@DRIVER.on_startup
async def startup():
    logger.opt(colors=True).info(logo)
    await database.connect()
    from LittlePaimon import admin
    await migrate_database()
    await check_resource()


DRIVER.on_shutdown(database.disconnect)
load_plugin('LittlePaimon.manager.bot_manager')
load_plugin('LittlePaimon.manager.plugin_manager')
load_plugin('LittlePaimon.manager.database_manager')
load_plugin('LittlePaimon.manager.alias_manager')
load_plugins(str(Path(__file__).parent / 'plugins'))
