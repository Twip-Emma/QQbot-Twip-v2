'''
Author: 七画一只妖
Date: 2022-02-18 20:21:44
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2022-10-10 10:38:25
Description: file content
'''
import json

import nonebot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import require
from nonebot.plugin import PluginMetadata

from .config import Config
from .data_source import get_leetcode_question_everyday

__plugin_meta__ = PluginMetadata(
    name='静默者-力扣算法',
    description='功能：每天固定三个时间发送每日一题',
    usage='''使用方式：无【静默模块】''',
    extra={'version': 'v1.3.5',
           'cost': '###0'}
)


global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler


#
# @scheduler.scheduled_job("cron", hour="*/2", id="xxx", args=[1], kwargs={"arg2": 2})
# async def run_every_2_hour(arg1, arg2):
#     pass


async def send_leetcode_everyday():
    question = get_leetcode_question_everyday()
    nonebot.log.logger.info("question:{}".format(question))
    # 转化成json格式
    jsonText = json.loads(question)
    # 题目题号
    no = jsonText.get('questionFrontendId')
    # 题名（中文）
    leetcodeTitle = jsonText.get('translatedTitle')
    # 提名 (英文)
    titleSlug = jsonText.get('titleSlug')
    # 题目难度级别
    level = jsonText.get('difficulty')
    # 题目内容
    context = jsonText.get('translatedContent')
    # 题目链接
    link = "https://leetcode-cn.com/problems/{}/".format(titleSlug) 
    message = "🤔编号：{}\n💾题目：{}\n🏷等级：{}\n📁链接：{}".format(no, leetcodeTitle, level, link)

    # 给配置的列表里的qq好友发leetcode通知
    for qq in plugin_config.leetcode_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=message)
    # 给群发送leetcode通知
    for qq_group in plugin_config.leetcode_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message="{}".format(message))


#调试用，可以每秒看到函数调用情况
#scheduler.add_job(send_leetcode_everyday, "interval", seconds=1, id="114514")

# 根据配置的参数，注册定时任务,每天发送
for index, time in enumerate(plugin_config.leetcode_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(send_leetcode_everyday, "cron", hour=time.hour, minute=time.minute, id=str(index))
