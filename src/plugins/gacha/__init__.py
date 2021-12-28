import nonebot
from nonebot import on_command, on_request, on_notice, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from typing import Union
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from datetime import datetime, timedelta
from nonebot.plugin import export
from .database import Pool

export = export()
export.Pool = Pool

gacha_cmd = on_command(
    cmd="十连",
    rule=regex("^十连$"),
    permission=GROUP_OWNER | GROUP_ADMIN,
    priority=5,
    block=True
)


@gacha_cmd.handle()
async def handle_request(bot: Bot, event: GroupMessageEvent, state: T_State):
    await gacha_cmd.finish('十连')
