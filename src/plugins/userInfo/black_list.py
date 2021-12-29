import nonebot
from nonebot import on_command, on_request, on_notice, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.plugin import require, plugins
import json
from .database import blackManager

add_black_cmd = on_command(
    cmd="拉黑",
    priority=5,
    block=True,
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
)

remove_black_cmd = on_command(
    cmd="取消拉黑",
    priority=5,
    block=True,
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
)


@add_black_cmd.handle()
async def handle_add_black_cmd(bot: Bot, event: GroupMessageEvent, state: T_State):
    text_list = []
    role_list = ["member", "admin", "owner", "superuser"]
    if str(event.sender.user_id) in bot.config.superusers:
        send_role = "superuser"
    else:
        send_role = event.sender.role
    for msg in event.get_message():
        if msg["type"] == "at":
            user_id = int(msg["data"]["qq"])
            user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id, no_cache=True)
            user_role = user_info["role"]
            if role_list.index(send_role) > role_list.index(user_role):
                blackManager.set_black(user_id)
                text_list.append(f"拉黑用户{user_info['nickname']}")
            else:
                text_list.append(f"你的权限不足以拉黑{user_info['nickname']}")
    await remove_black_cmd.finish("\n".join(text_list))


@remove_black_cmd.handle()
async def handle_remove_black_cmd(bot: Bot, event: GroupMessageEvent, state: T_State):
    text_list = []
    role_list = ["member", "admin", "owner", "superuser"]
    if event.sender.user_id in bot.config.superusers:
        send_role = "superuser"
    else:
        send_role = event.sender.role
    for msg in event.get_message():
        if msg["type"] == "at":
            user_id = int(msg["data"]["qq"])
            user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id, no_cache=True)
            user_role = user_info["role"]
            if role_list.index(send_role) > role_list.index(user_role):
                blackManager.set_white(user_id)
                text_list.append(f"取消拉黑用户{user_info['nickname']}")
            else:
                text_list.append(f"你的权限不足以取消拉黑{user_info['nickname']}")
    await remove_black_cmd.finish("\n".join(text_list))
