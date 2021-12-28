import yaml
from typing import Dict, List
from dataclasses import dataclass, field
import pathlib


def read_yaml_dict(path) -> Dict:
    with open(path, mode='r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_yaml_list(path) -> List:
    with open(path, mode='r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@dataclass
class DownloadFiles:
    @dataclass
    class _Files:
        face: List[str] = field(default_factory=list)
        style: List[str] = field(default_factory=list)
        class_: List[str] = field(default_factory=list)
        gacha: List[str] = field(default_factory=list)
        database: List[str] = field(default_factory=list)

        def to_dict(self) -> Dict[str, List[str]]:
            return {
                "face": self.face,
                "style": self.style,
                "class": self.class_,
                "gacha": self.gacha,
                "database": self.database
            }

    _path: pathlib.Path
    flies: _Files = field(default_factory=_Files)

    def __post_init__(self):
        tmp = read_yaml_dict(self._path)
        for k, v in tmp["files"].items():
            if k == "class":
                self.flies.__dict__["class_"] = v
            else:
                self.flies.__dict__[k] = v


@dataclass
class KeyWord:
    @dataclass
    class _Name:
        good: List[str] = field(default_factory=list)
        bad: List[str] = field(default_factory=list)

    @dataclass
    class _Keyword:
        good: List[str] = field(default_factory=list)
        bad: List[str] = field(default_factory=list)

    _path: pathlib.Path
    name: _Name = field(default_factory=_Name)
    keyword: _Keyword = field(default_factory=_Keyword)
    touch: List[str] = field(default_factory=list)

    def __post_init__(self):
        tmp = read_yaml_dict(self._path)
        for k, v in tmp["name"].items():
            self.name.__dict__[k] = v
        for k, v in tmp["keyword"].items():
            self.keyword.__dict__[k] = v
        self.touch = tmp["touch"]


@dataclass
class Nudge:
    _path: pathlib.Path
    str_list: List[str] = field(default_factory=list)

    def __post_init__(self):
        tmp = read_yaml_dict(self._path)
        self.str_list.extend(tmp["nudge"])

    def __getitem__(self, item):
        return self.str_list[item]


@dataclass
class Reward:
    @dataclass
    class _Reply:
        feeling: int = 0

    @dataclass
    class _Greeting:
        coupon: int = 0
        feeling: int = 0

    _path: pathlib.Path
    reply: _Reply = field(default_factory=_Reply)
    greeting: _Greeting = field(default_factory=_Greeting)

    def __post_init__(self):
        tmp = read_yaml_dict(self._path)
        for k, v in tmp["reply"].items():
            self.reply.__dict__[k] = v
        for k, v in tmp["greeting"].items():
            self.greeting.__dict__[k] = v
