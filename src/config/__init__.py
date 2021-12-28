from .path import PathConfig
from .configure import DownloadFiles, KeyWord, Nudge, Reward
import pathlib
from typing import Dict, List

pathConfig = PathConfig()

configure_path = pathlib.Path(__file__).parent / "configure"
downloadFiles = DownloadFiles(configure_path/"downloadFiles.yaml")
keyWord = KeyWord(configure_path/"keyword.yaml")
nudge = Nudge(configure_path/"nudge.yaml")
reward = Reward(configure_path/"reward.yaml")

