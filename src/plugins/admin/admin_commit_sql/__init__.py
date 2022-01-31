'''
Author: 七画一只妖
Date: 2022-01-31 10:58:01
LastEditors: 七画一只妖
LastEditTime: 2022-01-31 12:19:56
Description: file content
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent


# 设置管理员
SQL_SUPER = "1157529280" 


execute_sql = on_command('#sql', aliases={'#sql'})


@execute_sql.handle()
async def _(bot:Bot, event:GroupMessageEvent):
    user_id = str(event.user_id)
    if user_id != SQL_SUPER:
        await execute_sql.finish()
    message_context = str(event.get_message)
    
    # 获取想要执行的SQL语句
    user_sql = message_context.replace("#sql","").strip()

    # 判断执行SQL语句的类型
    change_type = ["delete","insert","update"]
    flag = False

    for item in change_type:
        if item in user_sql:
            flag = True
    
    if flag:
        pass
