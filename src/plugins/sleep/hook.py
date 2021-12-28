import nonebot
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, Bot
from nonebot.typing import T_State
from nonebot.message import run_preprocessor, IgnoredException
from .database import work_manager


@run_preprocessor
async def hook_is_work(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    if matcher.plugin_name != "sleep":
        if not work_manager.get_state(event.group_id).active:
            await bot.send(event, "博士，现在还不是工作时间哟")
            raise IgnoredException(f"{event.group_id} 正在休息")
