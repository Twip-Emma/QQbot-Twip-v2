'''
Author: 七画一只妖
Date: 2022-01-07 20:25:48
LastEditors: 七画一只妖
LastEditTime: 2022-09-17 14:29:43
Description: file content
'''
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

from os import path
import sys

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 定时任务
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})

# 测试模块
# nonebot.load_plugins("src/plugins/bean")
# nonebot.load_plugins("src/plugins/LittlePaimon")
# nonebot.load_plugin("LittlePaimon")

# 正式模块
# nonebot.load_plugins("src/plugins/admin")
nonebot.load_plugins("src/plugins/ys")
nonebot.load_plugins("src/plugins/function")
nonebot.load_plugins("src/plugins/user")
nonebot.load_plugins("src/plugins/listener")
nonebot.load_plugins("src/plugins/speaker")
nonebot.load_plugins("src/plugins/help")

# 加载绝对路径头
ABSOLUTE_PATH = path.join(path.dirname(__file__))

if __name__ == "__main__":
    sys.path.append(f"{ABSOLUTE_PATH}\\tool")
    sys.path.append(f"{ABSOLUTE_PATH}\\LittlePaimon")
    # sys.path.append(f"{ABSOLUTE_PATH}\\src\\plugins\\LittlePaimon")
    nonebot.run()
