import json
from src.config import pathConfig
import aiofiles
from typing import Dict
import pathlib


class GameData:
    cache: Dict[str, Dict]

    def __init__(self):
        self.cache = {}

    @staticmethod
    async def load(name: str) -> Dict:
        path = pathConfig.resource / f"{name}.json"
        async with aiofiles.open(path, "r", encoding="utf-8") as fp:
            tmp = await fp.read()
            return json.loads(tmp)

    async def load_all(self):
        for file in pathConfig.resource.iterdir():
            if file.suffix == ".json":
                data = await self.load(file.stem)
                self.cache[file.stem] = data
