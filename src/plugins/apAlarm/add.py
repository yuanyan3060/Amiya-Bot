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

scheduler = require("nonebot_plugin_apscheduler").scheduler
ap_cmd = on_message(
    rule=regex("^理智[0-9]*满[0-9]*"),
    priority=5,
    block=True
)

ap_pattern = re.compile(r'^理智([0-9]*)满([0-9]*)')


@ap_cmd.handle()
async def handle_ap(bot: Bot, event: MessageEvent, state: T_State):
    groups = ap_pattern.search(str(event.get_message())).groups()
    cur_ap, full_ap = int(groups[0]), int(groups[1])
    if cur_ap < 0 or full_ap <= 0:
        text = MessageSegment.text('啊这…看来博士是真的没有理智了……回头问问可露希尔能不能多给点理智合剂……\n')
        at = MessageSegment.at(event.user_id)
        await ap_cmd.finish(text + at)
    if cur_ap >= full_ap:
        text = MessageSegment.text('阿米娅已经帮博士记…呜……阿米娅现在可以提醒博士了吗\n')
        at = MessageSegment.at(event.user_id)
        await ap_cmd.finish(text + at)
    if full_ap > 135:
        text = MessageSegment.text('博士的理智有这么高吗？\n')
        at = MessageSegment.at(event.user_id)
        await ap_cmd.finish(text + at)

    full_time = (full_ap - cur_ap) * 6
    for i in scheduler.get_jobs():
        if i.name == "alarm":
            user_id, group_id, full_ap = i.args
            if user_id == event.user_id:
                scheduler.remove_job(i.id)
    if isinstance(event, GroupMessageEvent):
        job = scheduler.add_job(alarm, 'interval', minutes=full_time, args=[event.user_id, event.group_id, full_ap])
    else:
        job = scheduler.add_job(alarm, 'interval', minutes=full_time, args=[event.user_id, None, full_ap])

    text = MessageSegment.text('阿米娅已经帮博士记住了，回复满的时候阿米娅会提醒博士的哦～\n')
    at = MessageSegment.at(event.user_id)
    await ap_cmd.finish(text + at)


async def alarm(user_id: int, group_id: Optional[int], full_ap: int):
    bot: Bot = nonebot.get_bot()
    if group_id is None:
        await bot.send_private_msg(
            user_id=user_id,
            message=f"博士！博士！您的理智已经满{full_ap}了，快点上线查看吧～"
        )
    else:
        text = MessageSegment.text(f"博士！博士！您的理智已经满{full_ap}了，快点上线查看吧～\n")
        at = MessageSegment.at(user_id)
        await bot.send_group_msg(
            group_id=group_id,
            message=text + at
        )