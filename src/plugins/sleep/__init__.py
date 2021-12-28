import nonebot
from nonebot import on_command, on_request, on_notice, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, Bot
from nonebot.rule import keyword, startswith, to_me, regex
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from .database import work_manager
from datetime import datetime, timedelta
from . import hook
from ..util.common import calc_time_total

sleep_cmd = on_command(
    cmd="下班",
    rule=regex("^休息|下班$"),
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
    priority=5,
    block=True
)


@sleep_cmd.handle()
async def handle_request(bot: Bot, event: GroupMessageEvent, state: T_State):
    work_manager.set_sleep(event.group_id)
    await sleep_cmd.finish('打卡下班啦！博士需要阿米娅的时候再让阿米娅工作吧。^_^')


work_cmd = on_command(
    cmd="上班",
    rule=regex("^工作|上班$"),
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
    priority=5,
    block=True
)


@work_cmd.handle()
async def handle_request(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_state = work_manager.get_state(event.group_id)
    if group_state.active:
        await work_cmd.finish('阿米娅没有偷懒哦博士，请您也不要偷懒~')
    else:
        seconds: timedelta = datetime.now() - group_state.sleep_time
        total = calc_time_total(seconds)
        text = '打卡上班啦~阿米娅%s休息了%s……' % ('才' if seconds.total_seconds() < 600 else '一共', total)
        if seconds.total_seconds() < 600:
            text += '\n博士真是太过分了！哼~ >.<'
        else:
            text += '\n充足的休息才能更好的工作，博士，不要忘记休息哦 ^_^'
        work_manager.set_work(event.group_id)
        await sleep_cmd.finish(text)
