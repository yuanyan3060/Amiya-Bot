import peewee
from src.config import pathConfig
from typing import List, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass

sqlite_db = peewee.SqliteDatabase(pathConfig.database / 'GroupActive.db',
                                  pragmas={
                                      'timeout': 30
                                  },
                                  check_same_thread=False)


class GroupActive(peewee.Model):
    group_id = peewee.IntegerField(primary_key=True)
    active = peewee.BooleanField(default=True)
    sleep_time = peewee.DateTimeField()

    class Meta:
        database = sqlite_db


def get_group_active(group_id: int) -> GroupActive:
    groupActive = GroupActive.get_or_none(GroupActive.group_id == group_id)
    if groupActive is None:
        groupActive = GroupActive(group_id=group_id)
        groupActive.save(force_insert=True)
    return groupActive


class WorkManager:
    @dataclass
    class State:
        active: bool
        sleep_time: datetime

    GroupActiveList: Dict[int, State] = {}

    def __init__(self):
        for i in GroupActive.select():
            self.GroupActiveList[i.group_id] = self.State(i.active, i.sleep_time)

    def set_work(self, group_id: int):
        now = datetime.now()
        GroupActive.replace(group_id=group_id, active=True, sleep_time=now).execute()
        self.GroupActiveList[group_id] = self.State(True, now)

    def set_sleep(self, group_id: int):
        now = datetime.now()
        GroupActive.replace(group_id=group_id, active=False, sleep_time=now).execute()
        self.GroupActiveList[group_id] = self.State(False, now)

    def get_state(self, group_id: int):
        now = datetime.now()
        return self.GroupActiveList.get(group_id, self.State(True, now))


GroupActive.create_table()
work_manager = WorkManager()
