from dataclasses import asdict, dataclass
import json
from pathlib import Path
from loguru import logger
import dacite
from mvinstaller.fstools import get_sha1
from mvinstaller.addon_metadata import Metadata
from mvinstaller.signatures import DAT_VANILLA_SHA1, Mod

@dataclass(frozen=True)
class LastInstalledMods:
    sha1: str
    main: Mod
    addons: dict[str, Metadata]

def save_last_installed_mods(ftl_path, main: Mod, addons: dict[str, Metadata]):
    ftl_path = Path(ftl_path)
    logger.info('Saving the digest of the last installed mods...')
    dat_sha1 = get_sha1(ftl_path / 'ftl.dat')
    if dat_sha1 in DAT_VANILLA_SHA1:
        raise RuntimeError('Unexpected error: modded ftl.dat seems to be vanilla')

    lim = LastInstalledMods(dat_sha1, main, addons)
    with (ftl_path / 'last_installed_mods.json').open('w', encoding='utf-8') as f:
        json.dump(asdict(lim), f)

def load_last_installed_mods(ftl_path, dat_sha1):
    ftl_path = Path(ftl_path)
    try:
        json_path = ftl_path / 'last_installed_mods.json'
        if not json_path.is_file():
            return None
        
        with json_path.open('r', encoding='utf-8') as f:
            ret = dacite.from_dict(LastInstalledMods, json.load(f))
        
        if ret.sha1 != dat_sha1:
            raise RuntimeError('last_installed_mods.json: SHA1 mismatch')
        
        return ret
    except Exception as e:
        logger.warning(f'Unable to read last_installed_mods.json: {str(e)}')
        return None
