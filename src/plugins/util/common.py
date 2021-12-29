import os
import re
import time
import string
import random
import difflib
import datetime


def time_string_to_stamp(time_str: str, formatter: str = '%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(time.strptime(time_str, formatter)))


def word_in_sentence(sentence: str, words: list):
    for word in words:
        if word in sentence:
            return word
    return False


def check_sentence_by_re(sentence: str, words: list, names: list):
    for item in words:
        for n in names:
            if re.search(re.compile(item % n if '%s' in item else item), sentence):
                return True
    return False


def all_item_in_text(text: str, items: list):
    for item in items:
        if item not in text:
            return False
    return True


def find_similar_list(text: str, text_list: list, _random: bool = False):
    result = {}
    for item in text_list:
        rate = float(
            difflib.SequenceMatcher(None, text, item).quick_ratio() * len([n for n in text if n in set(item)])
        )
        if rate > 0:
            if rate not in result:
                result[rate] = []
            result[rate].append(item)

    if not result:
        return None, 0

    high = sorted(result.keys())[-1]
    result = result[high]

    if _random:
        return random.choice(result), high

    return result, high


def remove_xml_tag(text: str):
    return re.compile(r'<[^>]+>', re.S).sub('', text)


def insert_empty(text, max_num, half=False):
    return '%s%s' % (text, ('　' if half else ' ') * (max_num - len(str(text))))


def insert_zero(num: int):
    return ('0%d' % num) if num < 10 else str(num)


def integer(value):
    if type(value) is float and int(value) == value:
        value = int(value)
    return value


def random_code(length):
    pool = string.digits + string.ascii_letters
    code = ''
    for i in range(length):
        code += random.choice(pool)
    return code


def make_folder(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass


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
