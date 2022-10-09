from tool.find_power.format_data import is_level_S
from .manager import meme_manager, ActionResult, MemeMode
from .depends import split_msg, regex
from .data_source import memes
from .utils import Meme
from tool.nonebot_plugin_imageutils import BuildImage, Text2Image
import math
from io import BytesIO
from typing import List, Union
from PIL.Image import Image as IMG
from typing_extensions import Literal

from nonebot.params import Depends
from nonebot.utils import run_sync
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot import require, on_command, on_message
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent
)
from nonebot.adapters.onebot.v11.permission import (
    GROUP_ADMIN,
    GROUP_OWNER,
    PRIVATE_FRIEND,
)

# require("nonebot_plugin_imageutils")
# nb plugin install nonebot-plugin-imageutils


__plugin_meta__ = PluginMetadata(
    name="头像表情包",
    description="摸头等头像相关表情制作",
    usage="触发方式：指令 + @user/qq/自己/图片\n发送“头像表情包”查看支持的指令",
    extra={
        "unique_name": "petpet",
        "example": "摸 @小Q\n摸 114514\n摸 自己\n摸 [图片]",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.3.10",
    },
)

PERM_EDIT = GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND | SUPERUSER
PERM_GLOBAL = SUPERUSER

help_cmd = on_command(
    "头像表情包", aliases={"头像相关表情包", "头像相关表情制作"}, block=True, priority=1)
block_cmd = on_command("禁用表情", block=True, priority=1, permission=PERM_EDIT)
unblock_cmd = on_command("启用表情", block=True, priority=1, permission=PERM_EDIT)
block_cmd_gl = on_command("全局禁用表情", block=True,
                          priority=1, permission=PERM_GLOBAL)
unblock_cmd_gl = on_command(
    "全局启用表情", block=True, priority=1, permission=PERM_GLOBAL)


@run_sync
def help_image(user_id: str, memes: List[Meme]) -> BytesIO:
    def cmd_text(memes: List[Meme], start: int = 1) -> str:
        texts = []
        for i, meme in enumerate(memes):
            text = f"{i + start}. " + "/".join(meme.keywords)
            if not meme_manager.check(user_id, meme):
                text = f"[color=lightgrey]{text}[/color]"
            texts.append(text)
        return "\n".join(texts)

    head_text = "摸头等头像相关表情制作\n触发方式：指令 + @某人 / qq号 / 自己 / [图片]\n支持的指令："
    head = Text2Image.from_text(
        head_text, 30, weight="bold").to_image(padding=(20, 10))
    imgs: List[IMG] = []
    col_num = 3
    num_per_col = math.ceil(len(memes) / col_num)
    for idx in range(0, len(memes), num_per_col):
        text = cmd_text(memes[idx: idx + num_per_col], start=idx + 1)
        imgs.append(Text2Image.from_bbcode_text(
            text, 30).to_image(padding=(20, 10)))
    w = max(sum((img.width for img in imgs)), head.width)
    h = head.height + max((img.height for img in imgs))
    frame = BuildImage.new("RGBA", (w, h), "white")
    frame.paste(head, alpha=True)
    current_w = 0
    for img in imgs:
        frame.paste(img, (current_w, head.height), alpha=True)
        current_w += img.width
    return frame.save_jpg()


def get_user_id():
    def dependency(event: MessageEvent) -> str:
        return (
            f"group_{event.group_id}"
            if isinstance(event, GroupMessageEvent)
            else f"private_{event.user_id}"
        )

    return Depends(dependency)


def check_flag(meme: Meme):
    def dependency(user_id: str = get_user_id()) -> bool:
        return meme_manager.check(user_id, meme)

    return Depends(dependency)


@help_cmd.handle()
@is_level_S
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent], user_id: str = get_user_id()):
    img = await help_image(user_id, memes)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


@block_cmd.handle()
async def _(
    matcher: Matcher, msg: Message = CommandArg(), user_id: str = get_user_id()
):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.block(user_id, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 禁用成功"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 禁用失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@unblock_cmd.handle()
async def _(
    matcher: Matcher, msg: Message = CommandArg(), user_id: str = get_user_id()
):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.unblock(user_id, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 启用成功"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 启用失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@block_cmd_gl.handle()
async def _(matcher: Matcher, msg: Message = CommandArg()):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.change_mode(MemeMode.WHITE, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 已设为白名单模式"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 设置失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@unblock_cmd_gl.handle()
async def _(matcher: Matcher, msg: Message = CommandArg()):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.change_mode(MemeMode.BLACK, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 已设为黑名单模式"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 设置失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        @is_level_S
        async def handle(
            event: Union[GroupMessageEvent, PrivateMessageEvent],
            matcher: Matcher,
            flag: Literal[True] = check_flag(meme),
            res: Union[str, BytesIO] = Depends(meme.func),
        ):
            if not flag:
                return
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=False,
            priority=1,
        ).append_handler(handler(meme), parameterless=[split_msg()])


create_matchers()
