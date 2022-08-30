'''
Author: 七画一只妖
Date: 2022-08-28 09:24:43
LastEditors: 七画一只妖
LastEditTime: 2022-08-28 22:19:00
Description: file content
'''
import threading

from ..all_import import *  # noqa: F403, F401
from ..utils.download_resource.download_all_resource import (
    download_all_resource,
)

download_resource = on_command('下载全部资源')


@download_resource.handle()
@handle_exception('下载全部资源', '资源下载错误')
@is_level_S
async def send_download_resource_msg(
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    matcher: Matcher,
    args: Message = CommandArg(),
):
    if args:
        return
    qid = event.sender.user_id
    if qid not in SUPERUSERS:
        return
    await matcher.send('正在开始下载~可能需要较久的时间!')
    im = await download_all_resource()
    await matcher.finish(im)


async def startup():
    logger.info('[资源文件下载] 正在检查与下载缺失的资源文件，可能需要较长时间，请稍等')
    logger.info(f'[资源文件下载] {await download_all_resource()}')


threading.Thread(target=lambda: asyncio.run(startup()), daemon=True).start()
