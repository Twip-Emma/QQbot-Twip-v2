import nonebot.plugin
from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg

from tool.find_power.format_data import is_level_S
from tool.QsPilUtils2.dao import text_to_image

default_start = list(nonebot.get_driver().config.command_start)[0]
helper = on_command("help", priority=1, aliases={"帮助"})
# Matcher level info registering, still active in-use
helper.__help_name__ = 'help'
helper.__help_info__ = f'''{default_start}help  # 获取本插件帮助
{default_start}help list  # 展示已加载插件列表
{default_start}help <plugin_name>  # 调取目标插件帮助信息'''


@helper.handle()
@is_level_S
async def handle_first_receive(event: GroupMessageEvent, matcher: Matcher, cost=0, args: Message = CommandArg()):
    at = MessageSegment.at(event.get_user_id())
    if args:
        matcher.set_arg("content", args)
    else:
        message = f'''欢迎使用Nonebot2 Help Menu
                    支持使用的前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
                    {default_start}帮助  # 获取本插件帮助
                    {default_start}帮助 列表  # 展示已加载插件列表
                    {default_start}帮助 <功能名>  # 调取目标插件帮助信息
                    '''
        await helper.send(MessageSegment.image(f"file:///{text_to_image(message,15,(20,20))}"))


@helper.got("content")
async def get_result(event: GroupMessageEvent, content: Message = Arg()):
    at = MessageSegment.at(event.get_user_id())
    arg = content.extract_plain_text().strip()
    if arg == "列表":
        plugin_set = nonebot.plugin.get_loaded_plugins()
        plugin_names = []
        for plugin in plugin_set:
            # 可阅读的插件名称name
            name = ''
            try:
                name += plugin.metadata.name if plugin.metadata and plugin.metadata.name \
                    else plugin.module.__getattribute__("__help_plugin_name__")
            except:
                name = plugin.name
            # 插件版本号
            try:
                version = plugin.metadata.extra.get('version') \
                    if plugin.metadata else plugin.module.__getattribute__("__help_version__")
            except:
                version = ""

            # 插件消耗
            try:
                cost = plugin.metadata.extra.get('cost') \
                    if plugin.metadata else plugin.module.__getattribute__("__help_cost__")
            except:
                cost = ""

            plugin_names.append(f'{name}|{cost}|{version}')
        plugin_names.sort()
        newline_char = '\n'
        result = f'已加载插件：\n{newline_char.join(plugin_names)}\n请发送：帮助 <功能名>\n以调取目标插件帮助信息'
    else:
        # package name
        plugin = nonebot.plugin.get_plugin(arg)
        # try nickname/helpname
        if not plugin:
            plugin_set = nonebot.plugin.get_loaded_plugins()
            for temp_plugin in plugin_set:
                try:
                    name = temp_plugin.metadata.name if temp_plugin.metadata and temp_plugin.metadata.name \
                        else temp_plugin.module.__getattribute__("__help_plugin_name__")
                except:
                    name = temp_plugin.name
                if name == arg:
                    plugin = temp_plugin
        # not found
        if not plugin:
            result = f'{arg} 不存在或未加载，请确认输入了正确的插件名'
        else:
            results = []
            # if metadata set, use the general usage in metadata instead of legacy __usage__
            if plugin.metadata and plugin.metadata.name and plugin.metadata.usage:
                results.extend(
                    [f'{plugin.metadata.name}: {plugin.metadata.description}', plugin.metadata.usage])
            else:
                # legacy __usage__ or __doc__
                try:
                    results.extend([plugin.module.__getattribute__("__help_plugin_name__"),
                                    plugin.module.__getattribute__("__usage__")])
                except:
                    try:
                        results.extend([plugin.name, plugin.module.__doc__])
                    except AttributeError:
                        pass
            # Matcher level help, still legacy since nb2 has no Matcher metadata
            matchers = plugin.matcher
            infos = {}
            index = 1
            for matcher in matchers:
                try:
                    name = matcher.__help_name__
                except AttributeError:
                    name = None
                try:
                    help_info = matcher.__help_info__
                except AttributeError:
                    help_info = matcher.__doc__
                if name and help_info:
                    infos[f'{index}. {name}'] = help_info
                    index += 1
            if index > 1:
                results.extend(["", "序号. 命令名: 命令用途"])
                results.extend(
                    [f'{key}: {value}' for key, value in infos.items()
                     if key and value]
                )
            results = list(filter(None, results))
            result = '\n'.join(results)
    await helper.send(MessageSegment.image(f"file:///{text_to_image(result,15,(20,20))}"))
    
