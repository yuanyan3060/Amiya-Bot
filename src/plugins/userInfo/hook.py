import nonebot
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent, Bot
from nonebot.typing import T_State
from nonebot.message import run_preprocessor, IgnoredException
from .database import blackManager


@run_preprocessor
async def hook_is_black(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if blackManager.is_black(event.user_id):
        raise IgnoredException(f"{event.user_id} 处于黑名单中")
