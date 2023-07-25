'''
Author: 七画一只妖 1157529280@qq.com
Date: 2022-10-09 14:37:42
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-07-25 09:42:15
FilePath: \QQbot-Twip-v2\Twip\help\common_helper\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
Nonebot 2 Help Plugin
Author: XZhouQD
Since: 16 May 2021
"""
import nonebot
from nonebot.plugin import PluginMetadata

from .handler import helper

__plugin_meta__ = PluginMetadata(
    name='帮助菜单',
    description='查看当前机器人的功能列表',
    usage='''使用方式：帮助 [列表|<功能名>]''',
    extra={'version': 'v0.3.1',
           'cost': '无消耗'}
)


default_start = list(nonebot.get_driver().config.command_start)[0]

# Legacy way of self registering (use custom attributes)
# Deprecated for nonebot-plugin-help 0.3.1+, prefer PluginMetadata.extra['version']
# __help_version__ = '0.3.1'
# Deprecated for nonebot-plugin-help 0.3.0+, prefer PluginMetadata.name
# __help_plugin_name__ = "Nonebot2 Help Menu"
# Deprecated for nonebot-plugin-help 0.3.0+, prefer PluginMetadata.usage
# __usage__ = f'''欢迎使用Nonebot2 Help Menu
# 本插件提供公共帮助菜单能力
# 此Bot配置的命令前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
# '''

# New way of self registering (use PluginMetadata)
# __plugin_meta__ = nonebot.plugin.PluginMetadata(
#     name='Nonebot2 Help Menu',
#     description='Nonebot2轻量级帮助插件',
#     usage=f'''欢迎使用Nonebot2 Help Menu
# 本插件提供公共帮助菜单能力
# 此Bot配置的命令前缀：{" ".join(list(nonebot.get_driver().config.command_start))}

# {default_start}help  # 获取本插件帮助
# {default_start}help list  # 展示已加载插件列表
# {default_start}help <插件名>  # 调取目标插件帮助信息
# ''',
#     extra={'version': '0.3.1'}
# )
