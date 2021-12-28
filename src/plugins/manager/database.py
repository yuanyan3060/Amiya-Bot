import peewee
from src.config import pathConfig
from typing import List, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass

sqlite_db = peewee.SqliteDatabase(pathConfig.database / 'Disable.db',
                                  pragmas={
                                      'timeout': 30
                                  },
                                  check_same_thread=False)


class Disable(peewee.Model):
    group_id = peewee.IntegerField(primary_key=True)
    function_id = peewee.TextField()
    status = peewee.IntegerField()

    class Meta:
        database = sqlite_db
