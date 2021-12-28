import nonebot
from nonebot import on_command, on_request, on_notice, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER

query_char_cmd = on_command(
    cmd="查干员",
    priority=10,
    block=True
)


@query_char_cmd.handle()
async def handle_query_char(bot: Bot, event: MessageEvent, state: T_State):
   pass