import datetime
from pathlib import Path
from time import time
import re
import dacite
from loguru import logger
from mvinstaller.fstools import glob_posix
from mvinstaller.webtools import download
from mvinstaller.util import get_cache_dir
from mvinstaller.signatures import TranslatedMod, LISTFILE_EXPIRE_DURATION
import json

_TRANSLATION_FN_PATTERN = re.compile(
    r'^.+-(?P<version>[^-]+)-(?P<locale>[a-zA-Z_]+)\+(?P<commitid>[a-fA-F0-9xX]+)\.ftl$',
    re.IGNORECASE
)

def _parse_listfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        listfile = json.load(f)

    created_time = int(datetime.datetime.fromisoformat(listfile["published_at"]).timestamp())
    mods = []
    for asset in listfile["assets"]:
        try:
            url = asset["browser_download_url"]
            fn = asset["name"]
            
            match = _TRANSLATION_FN_PATTERN.match(fn)
            if match is None:
                continue

            mod = dacite.from_dict(TranslatedMod, {
                'download_targets': {url: fn},
                **match.groupdict()
            })
            mods.append(mod)
        except Exception:
            continue
    return created_time, mods

def from_github_release(url) -> list[TranslatedMod]:
    listfile_path = get_cache_dir() / f'listfile-{hash(url):x}'

    if listfile_path.exists():
        created_time, mods = _parse_listfile(listfile_path)
        if created_time + LISTFILE_EXPIRE_DURATION < time():
            logger.info('Listfile expired. Fetching new one...')
            download(url, listfile_path, True)
            created_time, mods = _parse_listfile(listfile_path)
    else:
        logger.info('Listfile not found. Fetching new one...')
        download(url, listfile_path, True)
        created_time, mods = _parse_listfile(listfile_path)

    return mods

def clear_expired_mods(smm_mod_files, translated_mods: list[TranslatedMod]):
    valid_files = [
        str(fn).lower()
        for translated_mod in translated_mods
        for fn in translated_mod.download_targets.values()
    ]

    for path in smm_mod_files:
        path = Path(path)
        if _TRANSLATION_FN_PATTERN.match(path.name) and (path.name.lower() not in valid_files):
            logger.info(f'Cleaning up expired mod: {path.name}...')
            path.unlink(True)