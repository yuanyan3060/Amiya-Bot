import nonebot
from nonebot import on_regex, on_request, on_notice, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER

help_cmd = on_regex(
    pattern="^(可以做什么|能做什么|会做什么|会干什么|会什么|有什么功能|功能|菜单)$",
    priority=10,
    block=True
)


@help_cmd.handle()
async def handle_help(bot: Bot, event: MessageEvent, state: T_State):
    await help_cmd.finish('博士，这是阿米娅的功能指引\nhttps://www.amiyabot.com/blog/function.html')


code_cmd = on_regex(
    pattern="^(代码|源码)$",
    priority=10,
    block=True
)


@code_cmd.handle()
async def handle_help(bot: Bot, event: MessageEvent, state: T_State):
    await code_cmd.finish('https://www.amiyabot.com/blog/function.html')
