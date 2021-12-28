from pydantic import BaseSettings
import pathlib


class PathConfig(BaseSettings):
    root = pathlib.Path(__file__).parent.parent
    resource = root / "resource"
    images = resource / "images"
    database = resource / "database"
    ignore = resource / "ignore.json"

    face = images / 'face'
    font = resource / 'font'
    gacha = images / 'gacha'
    class_ = images / 'class'
    database = resource / 'database'
    data = resource / "data"
    local_version_file = resource / 'version.txt'

    view = root / "view"

    font_file = resource/'font/AdobeHeitiStd-Regular.otf'
    logo_file = resource/'font/rabbit.png'
    logo_file_white = resource/'font/rabbit-white.png'
