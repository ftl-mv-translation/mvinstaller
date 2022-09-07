from collections import namedtuple
from pathlib import Path
from hashlib import sha1
from enum import Enum
import winreg
import vdf
from mvinstaller.signatures import FtlExecutableType, HyperspaceType, HyperspaceInfo, DAT_VANILLA_SHA1, FIXED_PATHS

_EXE_SHA1_TO_INFO = {
    e.value.sha1: e.value
    for e in FtlExecutableType
}

_HS_SHA1_TO_INFO = {
    e.value.sha1: e.value
    for e in HyperspaceType
}

FtlInstallationState = namedtuple(
    'FtlInstallationState',
    ('ftl_executable_info', 'hyperspace_installed', 'hyperspace_info', 'is_ftldat_vanilla', 'is_ftldat_backedup')
)

def get_sha1(path): 
    hash = sha1()
    with open(path, 'rb') as f:
        hash.update(f.read())
    return hash.hexdigest()

def get_ftl_installation_state(path):
    path = Path(path)

    if not ((path / 'FTLGame.exe').is_file() and (path / 'ftl.dat').is_file()):
        return None

    ftl_executable_info = _EXE_SHA1_TO_INFO.get(get_sha1(path / 'FTLGame.exe'), None)

    hyperspace_installed = (
        (path / 'Hyperspace.dll').is_file()
        and (path / 'lua-5.3.dll').is_file()
        and (path / 'xinput1_4.dll').is_file()
    )

    hyperspace_info = _HS_SHA1_TO_INFO.get(get_sha1(path / 'Hyperspace.dll'), None) if hyperspace_installed else None

    is_ftldat_vanilla = get_sha1(path / 'ftl.dat') in DAT_VANILLA_SHA1

    is_ftldat_backedup = (
        (path / 'ftl.dat.vanilla').is_file() and (get_sha1(path / 'ftl.dat.vanilla') in DAT_VANILLA_SHA1)
    )
    
    return FtlInstallationState(
        ftl_executable_info, hyperspace_installed, hyperspace_info, is_ftldat_vanilla, is_ftldat_backedup
    )

def find_steam_ftl_path():
    def try_getting_steam_path_from(key_under_hklm):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_under_hklm) as key:
                v, t = winreg.QueryValueEx(key, 'InstallPath')
                if t != winreg.REG_SZ:
                    raise FileNotFoundError 
                return str(v)
        except FileNotFoundError:
            return None
    
    # Find Steam installation
    steam_installation_path = (
        try_getting_steam_path_from(r'SOFTWARE\WOW6432Node\Valve\Steam')
        or try_getting_steam_path_from(r'SOFTWARE\Valve\Steam')
    )
    if steam_installation_path is None:
        return None
    steam_installation_path = Path(steam_installation_path)
    if not steam_installation_path.is_dir():
        return None

    # Find the list of library folders
    with (steam_installation_path / 'steamapps/libraryfolders.vdf').open('r', encoding='utf-8') as f:
        libraryfolder_data = vdf.load(f)
        libraryfolder_paths = [
            v['path']
            for v in libraryfolder_data['libraryfolders'].values()
        ]

    for libraryfolder_path in libraryfolder_paths:
        try:
            # 212680 is a steamappid for FTL
            appmanifest_path = Path(libraryfolder_path) / 'steamapps/appmanifest_212680.acf'
            if appmanifest_path.is_file():
                with appmanifest_path.open('r', encoding='utf-8') as f:
                    appmanifest_data = vdf.load(f)
                    ret = Path(libraryfolder_path) / 'steamapps/common' / appmanifest_data['AppState']['installdir']
                    if ret.is_dir():
                        return str(ret)
        except Exception:
            continue
    
    return None

def get_ftl_path_candidates(additional_paths=None) -> dict[str: (FtlInstallationState | Exception)]:
    try:
        steam_ftl_path = find_steam_ftl_path()
    except Exception:
        steam_ftl_path = None

    paths_to_check = []
    if steam_ftl_path:
        paths_to_check.append(steam_ftl_path)
    paths_to_check += FIXED_PATHS
    if additional_paths:
        paths_to_check += additional_paths

    paths_to_check = set(Path(path).resolve() for path in paths_to_check)
    
    ret = {}
    for path in sorted(paths_to_check):
        try:
            state = get_ftl_installation_state(path)
            if state is not None:
                ret[path] = state
        except Exception as e:
            ret[path] = e
    
    return ret

def get_latest_hyperspace() -> HyperspaceInfo:
    return next(e.value for e in HyperspaceType if e.value.latest)
