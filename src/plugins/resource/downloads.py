import pathlib
from nonebot import get_driver
from nonebot import require
import httpx
from src.config import pathConfig, downloadFiles
import traceback
from nonebot.log import logger
from typing import Optional
import json
import aiofiles
import re
import shutil
import asyncio


async def request_file(url) -> Optional[bytes]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
                      'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }
    # noinspection PyBroadException
    times = 10
    while times > 0:
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', url, headers=headers, timeout=50.0) as response:
                    if response.status_code == 200:
                        await response.aread()
                        return response.content
        except httpx.TimeoutException:
            times -= 1
        except Exception as e:
            logger.error(traceback.format_exc(), stdout=False)
        return None


async def request_string(url) -> Optional[str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
                      'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }
    # noinspection PyBroadException
    times = 10
    while times > 0:
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', url, headers=headers, timeout=50.0) as response:
                    if response.status_code == 200:
                        await response.aread()
                        return response.text
        except httpx.TimeoutException:
            times -= 1
        except Exception as e:
            logger.error(traceback.format_exc(), stdout=False)
        return None


class DownLoader:

    def __init__(self):
        self.bot_source = 'http://vivien8261.gitee.io/amiya-bot-resource'
        self.bot_console = 'http://vivien8261.gitee.io/amiya-bot-console'
        self.game_data_version_source = 'https://gitee.com/vivien8261/Arknights-Bot-Resource/raw/main/gamedata'
        self.game_data_source = 'http://vivien8261.gitee.io/arknights-bot-resource/gamedata'
        self.pics_source = 'https://vivien8261.gitee.io/arknights-bot-resource'
        self.pics_source_glob_api = 'https://api.github.com/repos/yuanyan3060/Arknights-Bot-Resource/contents'
        self.sem = asyncio.Semaphore(10)
        self.resource = [
            'levels/enemydata/enemy_database',
            'excel/enemy_handbook_table',
            'excel/handbook_info_table',
            'excel/battle_equip_table',
            'excel/char_patch_table',
            'excel/character_table',
            'excel/uniequip_table',
            'excel/charword_table',
            'excel/building_data',
            'excel/range_table',
            'excel/gacha_table',
            'excel/stage_table',
            'excel/skill_table',
            'excel/skin_table',
            'excel/item_table'
        ]
        self.source_bank = {}

    async def get_pic(self, _type, name, _save_ignore=True):
        async with self.sem:
            url = f'{self.pics_source}/{_type}/{name}'
            save_path = pathConfig.images / _type
            image_path = save_path / name
            save_path.mkdir(parents=True, exist_ok=True)
            if not image_path.exists():
                pic = await request_file(url)
                if pic:
                    async with aiofiles.open(image_path, mode='wb+') as _pic:
                        await _pic.write(pic)
                    return True
                else:
                    return False
            else:
                return True

    async def get_all_pic(self, force_update=False):
        logger.info('checking arknights-bot-resource update')
        version_file_path = pathConfig.images / "res_version"
        version: Optional[str] = None
        if version_file_path.exists():
            async with aiofiles.open(version_file_path, "r", encoding="UTF-8") as fp:
                version = await fp.read()
        version_url = f"{self.pics_source}/version"
        cur_version = await request_string(version_url)

        if cur_version == version and force_update:
            return

        raw_glob_data = await request_string(self.pics_source_glob_api)
        glob_data = json.loads(raw_glob_data)

        for j in ['avatar', 'enemy', 'item', 'portrait', 'skill']:
            for dir_data in glob_data:
                if dir_data["path"] == j:
                    file_data_url = dir_data["url"]
                    raw_file_data = await request_string(file_data_url)
                    file_data = json.loads(raw_file_data)
                    file_list = [i['name'] for i in file_data if "#" not in i['name']]
                    dirs = pathConfig.images / j
                    dirs.mkdir(parents=True, exist_ok=True)
                    local_file_list = [i.name for i in dirs.iterdir()]
                    count = len(local_file_list)
                    logger.info('{} {}/{}', j, count, len(file_list))
                    tasks = []
                    for file in file_list:
                        if file not in local_file_list:
                            tasks.append(self.get_pic(j, file))
                    if len(tasks) == 0:
                        continue
                    dones, _ = await asyncio.wait(tasks)
                    for task in dones:
                        if task.result():
                            count += 1
                    logger.info('{} {}/{}', j, count, len(file_list))

    async def get_json_data(self, name):
        if name not in self.source_bank:
            async with aiofiles.open(pathConfig.resource / f'{name}.json', mode='r', encoding='utf-8') as src:
                self.source_bank[name] = json.loads(await src.read())

        return self.source_bank[name]

    async def check_update(self) -> Optional[str]:
        logger.info('checking GameData update...')

        version = await request_string(f'{self.game_data_version_source}/excel/data_version.txt')

        if version is None:
            logger.info('GameData version file request failed.')
            return None

        local_ver = None
        if pathConfig.local_version_file.exists():
            async with aiofiles.open(pathConfig.local_version_file, mode='r') as v:
                text = await v.read()
                local_ver = text.strip('\n')

        r = re.search(r'VersionControl:(.*)\n', version)
        if r:
            latest_ver = r.group(1)
            if latest_ver != local_ver:
                async with aiofiles.open(pathConfig.local_version_file, mode='w+') as v:
                    await v.write(latest_ver)
                logger.info(f'new GameData version detected: latest {latest_ver} --> local {local_ver}')
                return latest_ver
            logger.info(f'GameData version is up to date: {latest_ver}')
        else:
            logger.info(f'GameData update check failed.')
        return None

    async def download_resource(self, use_cache=False):

        if await self.check_update() is None:
            use_cache = True

        for name in self.resource:
            url = '%s/%s.json' % (self.game_data_source, name)
            res_path = pathConfig.resource / f"{name.split('/')[-1]}.json"
            if use_cache and res_path.exists():
                continue
            data = await request_string(url)
            if data:
                async with aiofiles.open(res_path, mode='w+', encoding='utf-8') as src:
                    await src.write(data)
            else:
                if pathConfig.local_version_file.exists():
                    pathConfig.local_version_file.rmdir()
                raise Exception(f'data [{name}] download failed')

    async def download_bot_resource(self, refresh=False):
        for name, files in downloadFiles.flies.to_dict().items():
            if name == 'database':
                continue
            for file in files:
                save: pathlib.Path = pathConfig.resource / file
                url = f'{self.bot_source}/{file}'
                if not save.exists() or refresh:
                    save.parent.mkdir(parents=True, exist_ok=True)
                    data = await request_file(url)
                    if data:
                        async with aiofiles.open(save, mode='wb+') as src:
                            await src.write(data)
                        logger.info("Download {} Success", file)
                    else:
                        raise Exception(f'file [{name}] download failed')

    async def download_bot_console(self):
        logger.info('checking Console update...')

        version_file = await request_string(f'{self.bot_console}/.version')

        if version_file is None:
            return None

        file_list = version_file.strip('\n').split('\n')
        version = file_list.pop(0)

        local_ver = None
        local_version_file = pathConfig.view / 'version.txt'
        need_update = False
        if not local_version_file.exists():
            need_update = True
        else:
            async with aiofiles.open(local_version_file, mode='r') as lv:
                local_ver = await lv.read()
                if version != local_ver:
                    need_update = True

        if need_update:
            logger.info(f'new Console version detected: latest {version} --> local {local_ver}')
            if pathConfig.view.exists():
                shutil.rmtree(pathConfig.view, ignore_errors=True)
        else:
            logger.info(f'Console version is up to date: {version}')

        pathConfig.view.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(local_version_file, mode='w+') as lv:
            await lv.write(version)

        for file in file_list:
            view_path = pathConfig.view / file
            if not view_path.exists() or need_update:
                folder = view_path.parent
                folder.mkdir(parents=True, exist_ok=True)
                url = f'{self.bot_console}/dist/{file}'
                data = await request_file(url)
                if data:
                    async with aiofiles.open(view_path, mode='wb+') as src:
                        await src.write(data)
                else:
                    logger.error(f'file [{file}] download failed', stdout=False)

    @staticmethod
    async def get_ignore(reset=False):
        if pathConfig.ignore.exists():
            async with aiofiles.open(pathConfig.ignore, mode='r', encoding='utf-8') as file:
                text = await file.read()
                ignore = json.loads(text)
                if 'image_download' not in ignore:
                    ignore['image_download'] = []
                if 'weibo_download' not in ignore:
                    ignore['weibo_download'] = []
        else:
            ignore = {
                'image_download': [],
                'weibo_download': []
            }

        if reset:
            ignore['image_download'] = []
            async with aiofiles.open(pathConfig.ignore, mode='w+', encoding='utf-8') as file:
                await file.write(json.dumps(ignore, ensure_ascii=False))

        return ignore

    @staticmethod
    async def save_ignore(data):
        async with aiofiles.open(pathConfig.ignore, mode='w+', encoding='utf-8') as file:
            await file.write(json.dumps(data, ensure_ascii=False))


scheduler = require("nonebot_plugin_apscheduler").scheduler
downLoader = DownLoader()

driver = get_driver()


@driver.on_startup
async def update():
    await downLoader.download_bot_console()
    await downLoader.download_resource()
    await downLoader.download_bot_resource()
    await downLoader.get_all_pic()
