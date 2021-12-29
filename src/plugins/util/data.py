import json
from src.config import pathConfig
import aiofiles
from typing import Dict, Tuple
import pathlib



class GameData:
    cache: Dict[str, Dict]

    def __init__(self):
        self.cache = {}

    async def load(self, name: str) -> Dict:
        if name in self.cache:
            return self.cache[name]
        path = pathConfig.resource / f"{name}.json"
        async with aiofiles.open(path, "r", encoding="utf-8") as fp:
            tmp = await fp.read()
            return json.loads(tmp)

    async def load_all(self):
        for file in pathConfig.resource.iterdir():
            if file.suffix == ".json":
                data = await self.load(file.stem)
                self.cache[file.stem] = data

    async def reload_all(self):
        for file in pathConfig.resource.iterdir():
            if file.suffix == ".json":
                if file.stem in self.cache:
                    data = await self.load(file.stem)
                    self.cache[file.stem] = data

    async def get_char_id_data(self, name) -> Tuple[str, Dict]:
        char_table = await self.load("character_table.json")
        for char_id, char_data in char_table.items():
            if char_data["name"] == name:
                return char_id, char_data


game_data = GameData()
