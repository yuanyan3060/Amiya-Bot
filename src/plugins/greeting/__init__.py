import nonebot
from nonebot import on_command, on_request, on_notice, get_driver, on_regex
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=+8))
greeting_cmd = on_regex(
    pattern="^早上好|早安|中午好|午安|下午好|晚上好$",
    priority=9,
    block=True
)


@greeting_cmd.handle()
async def handle_help(bot: Bot, event: MessageEvent, state: T_State):
    now = datetime.now(tz=tz)
    hours = now.hour
    if 0 <= hours <= 5:
        text = f'Dr.{event.sender.nickname}，这么晚还不睡吗？要注意休息哦～'
    elif 5 < hours <= 11:
        text = f'Dr.{event.sender.nickname}，早上好～'
    elif 11 < hours <= 14:
        text = f'Dr.{event.sender.nickname}，中午好～'
    elif 14 < hours <= 18:
        text = f'Dr.{event.sender.nickname}，下午好～'
    else:
        text = f'Dr.{event.sender.nickname}，晚上好～'
    await greeting_cmd.finish(text)
