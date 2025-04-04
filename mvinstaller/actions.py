import zipfile
import shutil
import winreg
import re
from pathlib import Path
import json
from loguru import logger
from mvinstaller.addon_metadata import read_metadata
from mvinstaller.fstools import extract_without_path, glob_posix
from mvinstaller.last_installed_mods import save_last_installed_mods
from mvinstaller.multiverse import clear_expired_mods, get_mv_mainmods, get_addons
from mvinstaller.webtools import download
from mvinstaller.util import get_cache_dir, run_checked_subprocess_with_logging_output
from mvinstaller.ftlpath import get_ftl_installation_state, get_latest_hyperspace
from mvinstaller.localetools import get_locale_name
from mvinstaller.signatures import (
    DOWNGRADERS, SMM_URL, SMM_FILENAME, SMM_ROOT_DIR
)

def is_java_installed():
    def try_check_java_version_from(key_under_hklm):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_under_hklm) as key:
                v, t = winreg.QueryValueEx(key, 'CurrentVersion')
                if t != winreg.REG_SZ:
                    raise FileNotFoundError
                return str(v)
        except FileNotFoundError:
            return None
    version = (
        try_check_java_version_from(r'Software\JavaSoft\Java Runtime Environment')
        or try_check_java_version_from(r'Software\WOW6432Node\JavaSoft\Java Runtime Environment')
    )
    if version is None:
        return False
    match = re.match(r'^([0-9]+)\.([0-9]+)', version)
    if match is None:
        return False
    major, minor = tuple(int(num) for num in match.groups())
    return major >= 1 and minor >= 6

def downgrade_ftl(ftl_path, downgrader):
    assert downgrader is not None

    ftl_path = Path(ftl_path)
    cache_dir = get_cache_dir()

    if downgrader == 'steam':
        latest_hyperspace = get_latest_hyperspace()

        archive_url = latest_hyperspace.url
        archive_filename = latest_hyperspace.filename
        extract_paths = [
            'Windows - Extract these files into where FTLGame.exe is/patch/flips.exe',
            'Windows - Extract these files into where FTLGame.exe is/patch/patch.bps'
        ]
    else:
        archive_url, archive_filename = DOWNGRADERS[downgrader]
        extract_paths = [
            'patch/flips.exe',
            'patch/patch.bps'
        ]

    downgrader_extract_dir = cache_dir / 'downgraders' / downgrader
    download(archive_url, cache_dir / archive_filename, False)

    logger.info('Extracting archive...')
    with zipfile.ZipFile(cache_dir / archive_filename) as zipf:
        for path in extract_paths:
            extract_without_path(zipf, path, downgrader_extract_dir)
    
    logger.info('Backing up original EXE in FTLGame_orig.exe...')
    shutil.copyfile(ftl_path / 'FTLGame.exe', ftl_path / 'FTLGame_orig.exe')

    logger.info('Patching...')
    run_checked_subprocess_with_logging_output(
        [
            str(downgrader_extract_dir / 'flips.exe'),
            '-a',
            str(downgrader_extract_dir / 'patch.bps'),
            str(ftl_path / 'FTLGame.exe')
        ]
    )

def install_hyperspace(ftl_path):
    ftl_path = Path(ftl_path)
    cache_dir = get_cache_dir()
    latest_hyperspace = get_latest_hyperspace()

    download(latest_hyperspace.url, cache_dir / latest_hyperspace.filename, False)

    logger.info('Extracting archive...')
    with zipfile.ZipFile(cache_dir / latest_hyperspace.filename) as zipf:
        FILES = ['Hyperspace.dll', 'xinput1_4.dll']
        for fn in FILES:
            extract_without_path(zipf, f'Windows - Extract these files into where FTLGame.exe is/{fn}', ftl_path)

def install_mods(locale_mv, addons_name, ftl_path):
    ftl_path = Path(ftl_path)
    cache_dir = get_cache_dir()

    # Find vanilla dat
    logger.info('Finding vanilla dat file...')
    installation_state = get_ftl_installation_state(ftl_path)
    if not (installation_state.is_ftldat_vanilla or installation_state.is_ftldat_backedup):
        raise RuntimeError('Cannot find vanilla dat file.')
    use_backup = installation_state.is_ftldat_backedup

    def install_ftlman():
        logger.info('Downloading ftlman...')
        download(SMM_URL, cache_dir / SMM_FILENAME, False)

        logger.info('Extracting archive...')
        with zipfile.ZipFile(cache_dir / SMM_FILENAME) as zipf:
            zipf.extractall(cache_dir)
        smmbase = cache_dir / SMM_ROOT_DIR
        
        logger.info('Writing ftlman config...')
        with (smmbase / 'settings.json').open('w', encoding='utf-8') as f:
            json.dump({
                "mod_directory": str(smmbase / 'mods'),
                'ftl_directory': str(ftl_path)
                }, f)
        
        return smmbase
    
    def patch_mods(smmbase):
        clear_expired_mods(glob_posix(str(smmbase / 'mods/*')))

        mainmods = get_mv_mainmods()
        mainmod = next(mainmod for mainmod in mainmods if mainmod.locale == locale_mv)

        logger.info(
            f'[Target main mod] FTL: Multiverse {mainmod.version}, {get_locale_name(mainmod.locale)}'
        )
        for url, fn in mainmod.download_targets.items():
            download(url, smmbase / 'mods' / fn, False)

        logger.info(f'[Target addons] {", ".join(addons_name)}')
        addons = [addon for addon in get_addons() if addon.id in addons_name]

        # Download addon files
        addon_files_to_install = {}
        for addon in addons:
            for url, fn in addon.download_targets.items():
                addon_files_to_install[url] = fn
        for url, fn in addon_files_to_install.items():
            download(url, smmbase / 'mods' / fn, False)

        # Get metadata that were actually installed
        addon_metadata = {}
        for addon in addons:
            # Use the first mod in the file list
            fn = next(iter(addon.download_targets.values()))
            with zipfile.ZipFile(smmbase / 'mods' / fn) as zipf:
                extract_without_path(zipf, 'mod-appendix/metadata.xml', cache_dir)
            addon_metadata[addon.id] = read_metadata(cache_dir / 'metadata.xml', addon.id)

        if not use_backup:
            logger.info('Creating backup for dat...')
            shutil.copy(ftl_path / 'ftl.dat', ftl_path / 'ftl.dat.vanilla')
        
        logger.info('Running patch...')
        mods = sorted([mainmod] + addons, key=lambda mod: mod.priority)
        run_checked_subprocess_with_logging_output(
            [
                smmbase / 'ftlman.exe',
                'patch',
                *(
                    download_target
                    for mod in mods
                    for download_target in mod.download_targets.values()
                )
            ]
        )
        return mainmod, addon_metadata
    smmbase = install_ftlman()
    mainmod, addon_metadata = patch_mods(smmbase)
    save_last_installed_mods(ftl_path, mainmod, addon_metadata)
