<!--
 * @Author: 七画一只妖
 * @Date: 2022-01-07 20:25:48
 * @LastEditors: 七画一只妖 1157529280@qq.com
 * @LastEditTime: 2023-08-29 14:36:55
 * @Description: file content
-->
<p align="center">
  <a href="https://cdngoapl.twip.top/%E7%94%A8%E6%88%B7%E5%A4%87%E9%80%89%E5%A4%B4%E5%83%8F/86.%E5%B7%AB%E5%A5%B3%E7%BC%87fix.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# Twip

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 基于异步机器人框架Nonebot开发的机器人 ✨_
<!-- prettier-ignore-end -->

</div>

<p align="center">

![maven](https://img.shields.io/badge/python-3.9%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0beta5-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0rc3-red)

</p>

# Twip-v2 
#### 最新版本更新至：v2.0.0beta3

## 基本介绍

### 常见问题Q/A
**这个机器人我拉进去可以直接用吗？**
> 不可以，需要开发者手动将群加入权限列表中，你可以选择功能开多少（权限S或者A）功能开太多会刷屏，谨慎选择

**这个机器人功能/技术是自己做的吗？**
> 使用了[Nonebot2](https://nb2.baka.icu/)和[gocqhttp](https://docs.go-cqhttp.org/)，机器人的功能大部分是自己写的，有一部分功能参考了其他插件/项目的写法或者规范，直接照搬插件商店的功能文件夹前均加上了nonebot_plugins字样，进入[Nonebot插件商店](https://nb2.baka.icu/store)都能搜得到，（大佬们太强了~

**我下载项目之后可以直接运行吗？**
> 并不能，因为本仓库我自己编写了tool模块并且融合进了每个功能，该tool模块包含了工具类、配置文件、加密算法等并未上传，所以你只能取其某个功能并修改相关代码才能运行成功

**机器人有什么亮点？**
> 部分算法、IO流程、缓存机制什么的应该算吧，毕竟机器人的总用户高达11000位，活跃用户虽然只有1000位左右，但是这些人在同一时刻高频使用机器人的话，自己写的代码性能优劣就体现出来了。难忘的一点是，甚至有的人通过群昵称对我的机器人进行SQL注入，真是防不胜防呀

**你做这个项目学到了什么**
> 学习到了如何很好的对一个较大的项目进行管理，包括模块与模块之间的耦合度，响应时间，组件复用情况怎么样等等。由于记录发言记录的数据库（MySQL）表的数据是百万级别的，这时候又巩固了如何优化数据库的知识。用户过多，某一时刻使用量过大时，如何处理高并发的问题的解决思路等等

### 参考指令
> 详细指令可通过 `帮助 <所属模块名称>` 查看

| 所属模块 | 行动点消耗 | 版本 |
|  ----  | ----  |----  |
| Twip | 0 | v2.0.0beta3 |
nonebot_plugin_apscheduler|0|-
nonebot_plugin_imageutils|0|-
万象抽卡|30|v1.0.0
个人信息|0|v1.0.0
以图搜图|40|v0.0.1
原神抽卡|40|v1.0.0
头像表情|13|0.3.13
帮助菜单|0|v0.3.1
查看状态|0|v1.0.0
水群排行|10|v1.0.0
求签系统|15|v1.0.0
电费查询|5|v1.0.0
群友老婆|65|v0.0.1
锁定用户|0|v1.0.0
陪聊系统|2|v1.0.0
静默者-信息更新|0|v0.0.1
静默者-健康回复|0|v0.0.1
静默者-力扣算法|0|v1.3.5
静默者-消息记录|0|v0.0.1
静默者-闪照撤回|0|v0.0.1


### 开始部署/使用某个功能

#### 1.直接部署
1.在根目录创建`.env.prod`文件进入并输入以下配置
~~~.env.prod
HOST=127.0.0.1
SECRET=
ACCESS_TOKEN=

PORT=8080  # 配置 NoneBot 监听的端口
DEBUG=false  # 开启 debug 模式 **请勿在生产环境开启**
SUPERUSERS=[""]  # 配置 NoneBot 超级用户
NICKNAME=[""]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符
LOG_LEVEL=SUCCESS

# 力扣
LEETCODE_QQ_FRIENDS=[]
LEETCODE_QQ_GROUPS=[123,456]
LEETCODE_INFORM_TIME=[{"HOUR":8,"MINUTE":10},{"HOUR":12,"MINUTE":10},{"HOUR":17,"MINUTE":10}]

# 搜图插件
EX_COOKIE=
PROXY=
SEARCH_LIMIT=10
RISK_CONTROL=true
RECORD_PRIORITY=99

# 直链提取器
linker_group=["123"]

# 数据库连接
db_url="数据库连接"
db_card="账号"
db_pass="密码"
db_lib="数据库名称"

# 茉莉云
mly_key="茉莉云key"
mly_secret='茉莉云secret'
~~~

2.执行以下SQL语句
> 进入根目录的`sql`文件，把里面的sql文件全部执行一遍即可

#### 2.使用某个功能（解耦）
> 注意：本部署教程并不是整个机器人的部署教程，在观看前，你需要有一定的Python基础以及机器人的部署经验

**我们拿天气查询功能为例，找到`src/plugins/function/weather`打开`__init__.py`**

1.删除以下代码（开头导入模块那里）
~~~Python
from tool.find_power.format_data import is_level_S
~~~

2.找到这一块代码
~~~Python
@weather.handle()
async def handle_first_receive(event: MessageEvent):
    if not is_level_S(event):
        await weather.finish()
    global CITY
    args = str(event.get_message()).split()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    try:
        # city_weather = await get_weather(args[1])
        city_weather = await get_weather_of_city(city=args[1])
        await weather.send(message=city_weather)
    except:
        await weather.send("请输入你要查询的天气\n比如发送：天气 北京")
~~~

删除其中的
~~~Python
if not is_level_S(event):
    await weather.finish()
~~~

**重启你的机器人然后艾特机器人并发送`天气 北京`得到响应即代表安装成功**