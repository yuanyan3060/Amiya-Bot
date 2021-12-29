import peewee
from src.config import pathConfig
from typing import List, Dict, Set
from datetime import datetime, timedelta
from dataclasses import dataclass

sqlite_db = peewee.SqliteDatabase(pathConfig.database / 'User.db',
                                  pragmas={
                                      'timeout': 30
                                  },
                                  check_same_thread=False)


class User(peewee.Model):
    user_id = peewee.IntegerField(primary_key=True)
    user_feeling = peewee.IntegerField(default=0)
    user_mood = peewee.IntegerField(default=15)
    message_num = peewee.IntegerField(default=0)
    coupon = peewee.IntegerField(default=50)
    gacha_break_even = peewee.IntegerField(default=0)
    gacha_pool = peewee.IntegerField(default=1)
    sign_in = peewee.IntegerField(default=0)
    sign_times = peewee.IntegerField(default=0)
    black = peewee.BooleanField(default=False)
    waiting = peewee.TextField(null=True)

    class Meta:
        database = sqlite_db


User.create_table()


class BlackManager:
    _black_set: Set[int]

    def __init__(self):
        self._black_set = set()
        for i in User.select():
            if i.black:
                self._black_set.add(i.user_id)

    def is_black(self, user_id: int):
        return user_id in self._black_set

    def set_black(self, user_id: int):
        User.replace(user_id=user_id, black=True).execute()
        self._black_set.add(user_id)

    def set_white(self, user_id: int):
        User.replace(user_id=user_id, black=False).execute()
        self._black_set.remove(user_id)


blackManager = BlackManager()
