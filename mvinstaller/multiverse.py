import datetime
from pathlib import Path
from time import time
import re
import json
import urllib.parse
from loguru import logger
from mvinstaller.webtools import download
from mvinstaller.util import get_cache_dir, sha256
from mvinstaller.signatures import (
    Mod,
    RELEASE_EXPIRE_DURATION,
    MAINMODS_TRANSLATION_RELEASE,
    ADDONS_TRANSLATION_RELEASE,
    FixedAddonsList
)

_TRANSLATION_FN_PATTERN = re.compile(
    r'^(?P<id>.+)-(?P<version>v?[0-9\.]+(?:-.*)?)-(?P<locale>[a-zA-Z_]+)\+(?P<commitid>[a-fA-F0-9xX]+)\.ftl$',
    re.IGNORECASE
)

def _parse_release(path):
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
            match = match.groupdict()

            mod = Mod(
                id=f"{match['id']}/{match['locale']}",
                download_targets={url: fn},
                locale=match['locale'],
                version=f"{match['version']}+{match['commitid']}",
                metadata_url=url.replace(
                    urllib.parse.quote_plus(fn),
                    urllib.parse.quote_plus(f"metadata-{match['locale']}.xml")
                ),
                compatible_mv_locale=[match['locale']]
            )
            mods.append(mod)
        except Exception:
            continue
    return created_time, mods

def from_github_release(url) -> list[Mod]:
    release_cache_path = get_cache_dir() / f'release-{sha256(url)}.json'

    if release_cache_path.exists():
        created_time, mods = _parse_release(release_cache_path)
        if created_time + RELEASE_EXPIRE_DURATION < time():
            logger.info('Release file expired. Fetching new one...')
            download(url, release_cache_path, True)
            created_time, mods = _parse_release(release_cache_path)
    else:
        logger.info('Release file not found. Fetching new one...')
        download(url, release_cache_path, True)
        created_time, mods = _parse_release(release_cache_path)
    return mods

def get_mv_mainmods() -> list[Mod]:
    return from_github_release(MAINMODS_TRANSLATION_RELEASE)

def get_addons() -> list[Mod]:
    return (
        [mod for url in ADDONS_TRANSLATION_RELEASE for mod in from_github_release(url)]
        + [e.value for e in FixedAddonsList]
    )

def clear_expired_mods(smm_mod_files):
    mods = get_mv_mainmods() + get_addons()
    mods_files = [str(fn).lower() for mod in mods for fn in mod.download_targets.values()]

    for path in smm_mod_files:
        path = Path(path)
        if path.name.lower() not in mods_files:
            logger.info(f'Cleaning up expired mod: {path.name}...')
            path.unlink(True)
