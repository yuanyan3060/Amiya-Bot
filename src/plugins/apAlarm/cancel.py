import nonebot
from nonebot import on_command, on_request, on_notice, get_driver, on_message
from nonebot.adapters.cqhttp import MessageSegment, Message, MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from typing import Optional
import re
import time
from nonebot import require
import datetime

scheduler = require("nonebot_plugin_apscheduler").scheduler
ap_cancel_cmd = on_command(
    cmd="取消提醒",
    rule=regex("^取消提醒$"),
    priority=5,
    block=True
)


@ap_cancel_cmd.handle()
async def handle_ap_cancel(bot: Bot, event: MessageEvent, state: T_State):
    print(444444)
    for i in scheduler.get_jobs():
        if i.name == "alarm":
            user_id, group_id, full_ap = i.args
            if user_id == event.user_id:
                scheduler.remove_job(i.id)
                text = '博士，理智提醒已经取消了\n'
                at = MessageSegment.at(event.user_id)
                await ap_cancel_cmd.finish(text+at)
    text = '阿米娅还没有帮博士记录理智提醒哦\n'
    at = MessageSegment.at(event.user_id)
    await ap_cancel_cmd.finish(text + at)
    await ap_cancel_cmd.finish('阿米娅还没有帮博士记录理智提醒哦')
