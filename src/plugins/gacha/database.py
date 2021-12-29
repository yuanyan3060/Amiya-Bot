import peewee
from src.config import pathConfig
from typing import List, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass

sqlite_db = peewee.SqliteDatabase(pathConfig.database / 'Pool.db',
                                  pragmas={
                                      'timeout': 30
                                  })


class Pool(peewee.Model):
    pool_id = peewee.IntegerField(primary_key=True, constraints=[peewee.SQL('autoincrement')])
    pool_name = peewee.TextField(unique=True, default="适合多种场合的强力干员")
    pickup_6 = peewee.TextField(null=True, default="")
    pickup_5 = peewee.TextField(null=True, default="")
    pickup_4 = peewee.TextField(null=True, default="")
    pickup_s = peewee.TextField(null=True, default="")
    limit_pool = peewee.IntegerField(default=0)

    class Meta:
        database = sqlite_db


Pool.create_table()
