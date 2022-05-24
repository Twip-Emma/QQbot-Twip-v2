<!--
 * @Author: 七画一只妖
 * @Date: 2022-01-07 20:25:48
 * @LastEditors: 七画一只妖
 * @LastEditTime: 2022-05-24 19:40:12
 * @Description: file content
-->
# Twip-v2

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
| 所属模块 | 功能描述 | 权限要求 | 参考指令 |
| ----------- | ----------- | ----------- | ----------- |
| 用户模块 | 获得一张运势图  |S|求签|
| 用户模块 | 签到，并且一定量货币，每日只能签到一次 |S|签到|
|发言模块|艾特机器人并且发出你想说的话即可获得回复|A|无|
|发言模块|“戳一戳”机器人获得机器人运行状态消息|-|无|
|聆听模块|数据库连接自动更新|-|无|
|聆听模块|每天8点12点17点发送力扣每日一题（算法）|-|无|
|聆听模块|记录每条发言|-|无|
|聆听模块|米游社每日签到（原神打卡）|-|无|
|聆听模块|定时检查数据库内的乱码错误并修正|-|无|
|聆听模块|群友大乱斗根据一定的规则回复生命值、MP值、攻防智力比等|-|无|
|帮助模块|获得简易指令列表|S|帮助、帮助 功能组模块、...|
| 功能模块 | 获取指定城市的最近3天天气|S|天气|
| 功能模块 |生成一个你懂得的P站图标风格的图片|S|ph图标 <参数1> <参数2>|
|功能模块|获得一张万象物语抽卡结果图，每日有限制抽卡次数|A|起源十连、限定十连、首发十连、雪莉十连、爱丽丝十连|
|功能模块|获得一张原神抽卡结果图，每日有限制抽卡次数|A|原神十连|
|功能模块|Arcaea获取B30等功能|S|arcinfo|
|功能模块|根据PID搜索图片（来自P站）|S|搜索图片 88888888|
|功能模块|随机涩图、根据指定xp搜索涩图（来自P站）|S|随机涩图、标签涩图 萝莉 白丝（等参数）|
|功能模块|这人生不想呆了，我选择重开|S|重开|
|功能模块|讲一句话抽象成emoji表情|S|抽象 大家上午好呀|
|功能模块|菜梦AI续写文章功能|S|（艾特机器人）续写 XXX|
|功能模块|多渠道搜图功能|S|搜图 （发送一张图片）|
|功能模块|随机唐可可功能（眼力挑战，全群可触发、全群可抢答）|S|随机唐可可|
|功能模块|群友大乱斗功能，发送帮助以获得更多指令（已弃用）|S|乱斗帮助|
|功能模块|群友的水群排行，从机器人诞生的那一刻开始统计，跨群通用|S|查看水群排行|


### 开始部署/使用某个功能
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