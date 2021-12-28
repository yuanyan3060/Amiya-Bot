import datetime


def calc_time_total(t: datetime.timedelta):
    day = t.days
    hour, remainder = divmod(t.total_seconds(), 3600)
    mint, sec = divmod(remainder, 60)
    hour, mint, sec = int(hour), int(mint), int(sec)
    total = ''
    if day:
        total += '%d天' % day
    if hour:
        total += '%d小时' % hour
    if mint:
        total += '%d分钟' % mint
    if sec and not (day or hour or mint):
        total += '%d秒' % sec

    return total
