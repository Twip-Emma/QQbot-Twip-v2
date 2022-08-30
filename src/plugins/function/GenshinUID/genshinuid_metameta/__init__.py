'''
Author: 七画一只妖
Date: 2022-08-28 09:24:43
LastEditors: 七画一只妖
LastEditTime: 2022-08-28 21:45:52
Description: file content
'''
from typing import Optional

from nonebot.plugin import PluginMetadata

sub_menus = []
__plugin_meta__ = PluginMetadata(
    name='GenshinUID',
    description='基于NoneBot2的原神Uid查询/原神Wiki/米游社签到/树脂提醒插件',
    usage=(
        '发送 gs帮助 可以获取帮助列表，也可以参考下面的表格\n'
        '可以使用 [菜单 gsuid 序号] 获取某功能详细介绍\n'
        '示例指令括号中的内容为可选参数，可以省略'
    ),
    extra={'menu_data': sub_menus, 'menu_template': 'default'},
)


def register_menu_func(
    func: str,
    trigger_condition: str,
    brief_des: str,
    trigger_method: str = '指令',
    detail_des: Optional[str] = None,
):
    sub_menus.append(
        {
            'func': func,
            'trigger_method': trigger_method,
            'trigger_condition': trigger_condition,
            'brief_des': brief_des,
            'detail_des': detail_des or brief_des,
        }
    )


def register_menu(*args, **kwargs):
    def decorator(f):
        register_menu_func(*args, **kwargs)
        return f

    return decorator
