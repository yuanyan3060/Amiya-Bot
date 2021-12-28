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
ap_query_cmd = on_message(
    rule=regex("^(多少理智)|(理智.*多少)$"),
    priority=5,
    block=True
)


@ap_query_cmd.handle()
async def handle_ap_query(bot: Bot, event: MessageEvent, state: T_State):
    for i in scheduler.get_jobs():
        if i.name == "alarm":
            user_id, group_id, full_ap = i.args
            if user_id==event.user_id:
                next_run_time: datetime.datetime = i.next_run_time
                full_time = next_run_time.strftime('%Y-%m-%d %H:%M:%S')
                through = int(next_run_time.timestamp() - time.time())
                restored = int(full_ap-through / 360)
                text = '博士，根据上一次记录，您的 %d 理智会在 %s 左右回复满\n' \
                       '不计算上限的话，现在已经回复到 %d 理智了' % (full_ap, full_time, restored)
                await ap_query_cmd.finish(text)
    await ap_query_cmd.finish('阿米娅还没有帮博士记录理智提醒哦')
