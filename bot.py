'''
Author: 七画一只妖
Date: 2022-01-07 20:25:48
LastEditors: 七画一只妖
LastEditTime: 2022-01-18 21:00:16
Description: file content
'''
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from os import path
import sys

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

# 测试模块
nonebot.load_plugins("src/plugins/bean")

# 正式模块
nonebot.load_plugins("src/plugins/function")
nonebot.load_plugins("src/plugins/user")

# 加载绝对路径头
ABSOLUTE_PATH = path.join(path.dirname(__file__))

if __name__ == "__main__":
    sys.path.append(f"{ABSOLUTE_PATH}\\tool")
    nonebot.run()