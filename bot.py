'''
Author: 七画一只妖
Date: 2022-01-07 20:25:48
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-08-29 14:18:55
Description: file content
'''
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
# from nonebot.log import logger, logger_id
# logger.remove(logger_id)


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

# 正式模块
# nonebot.load_plugins("src/plugins/admin")
# nonebot.load_plugins("src/plugins/function")
# nonebot.load_plugins("src/plugins/user")
# nonebot.load_plugins("src/plugins/listener")
# nonebot.load_plugins("src/plugins/speaker")
# nonebot.load_plugins("src/plugins/help")

# 单模块
nonebot.load_plugin("Twip")

# 全局模块
# nonebot.load_plugin()

# 加载绝对路径头
ABSOLUTE_PATH = path.join(path.dirname(__file__))

if __name__ == "__main__":
    sys.path.append(f"{ABSOLUTE_PATH}\\tool")
    nonebot.run()
