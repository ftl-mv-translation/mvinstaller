from pathlib import Path
from time import time
import re
import dacite
from loguru import logger
from mvinstaller.webtools import download
from mvinstaller.util import get_cache_dir
from mvinstaller.signatures import MainMod, LISTFILE_EXPIRE_DURATION, LISTFILE_URL

_TRANSLATION_FN_PATTERN = re.compile(
    r'^FTL-Multiverse-(?P<version>.+)-(?P<locale>[a-zA-Z_]+)\+(?P<commitid>[a-fA-F0-9xX]+)\.ftl$',
    re.IGNORECASE
)

def _parse_translation_listfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [line for line in lines if line]

    created_time = int(lines[0])
    mainmods = []
    for url in lines[1:]:
        try:
            fn = url.split('/')[-1]
            
            match = _TRANSLATION_FN_PATTERN.match(fn)
            if match is None:
                continue
            match = match.groupdict()
            
            mainmod = MainMod(
                download_targets={url: fn},
                locale=match['locale'],
                version=f"{match['version']}+{match['commitid']}"
            )
            mainmods.append(mainmod)
        except Exception:
            continue
    return created_time, mainmods

def get_mv_mainmods() -> list[MainMod]:
    listfile_path = get_cache_dir() / 'listfile'

    if listfile_path.exists():
        created_time, mainmods = _parse_translation_listfile(listfile_path)
        if created_time + LISTFILE_EXPIRE_DURATION < time():
            logger.info('Listfile expired. Fetching new one...')
            download(LISTFILE_URL, listfile_path, True)
            created_time, mainmods = _parse_translation_listfile(listfile_path)
    else:
        logger.info('Listfile not found. Fetching new one...')
        download(LISTFILE_URL, listfile_path, True)
        created_time, mainmods = _parse_translation_listfile(listfile_path)

    # Exclude the English version (see #3)
    # return [MV_ENGLISH_MAINMOD] + mainmods
    return mainmods

def clear_expired_mainmods(smm_mod_files):
    mainmods = get_mv_mainmods()
    mainmods_files = [str(fn).lower() for mainmod in mainmods for fn in mainmod.download_targets.values()]

    for path in smm_mod_files:
        path = Path(path)
        if _TRANSLATION_FN_PATTERN.match(path.name) and (path.name.lower() not in mainmods_files):
            logger.info(f'Cleaning up expired mod: {path.name}...')
            path.unlink(True)
