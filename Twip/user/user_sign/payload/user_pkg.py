'''
Author: 七画一只妖 1157529280@qq.com
Date: 2023-11-12 12:30:25
LastEditors: 七画一只妖 1157529280@qq.com
LastEditTime: 2023-11-12 13:00:39
'''
from .db import sql_dql
from .get_image import get_sign_image
import datetime

"""
DROP TABLE IF EXISTS "user_sign";
CREATE TABLE "user_sign" (
  "id" text NOT NULL,
  "user_id" text,
  "time" text,
  "sign" text,
  PRIMARY KEY ("id")
);
"""

# 签到流程
async def get_sign(user_id: str, user_name: str) -> str:
    sign_data = await sql_dql(
        "select sign from user_sign where user_id=? and time=?",
        (
            user_id,
            datetime.datetime.now().strftime("%Y-%m-%d")
        )
    )
    point_list = None
    if sign_data != []:
        point_list = parse_coordinates_string(sign_data[0][0])
    return await get_sign_image(
        user_id=user_id,
        user_name=user_name,
        random_circle_coordinates=point_list
    )


# 数据转换-str转list
def parse_coordinates_string(coordinates_string):
    # 移除首尾的方括号，并按逗号分隔字符串
    coordinates_list = coordinates_string.strip('[]').replace("(","").replace(")","").split(",")

    # 提取每个坐标点的 x 和 y，并转换为整数
    parsed_coordinates = [(int(coordinates_list[i]), int(coordinates_list[i + 1])) for i in range(0, len(coordinates_list), 2)]

    return parsed_coordinates