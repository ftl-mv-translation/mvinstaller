from dataclasses import dataclass
from enum import Enum
from typing import Optional

########## Type definitions

@dataclass(frozen=True)
class FtlExecutableInfo:                # A signature of FTLGame.exe
    name: str                           # The version displayed in the installer app
    downgraded: bool                    # Whether it's downgraded and can be modded with Hyperspace
    downgrader: Optional[str]           # Specify the name of the downgrader to be passed in `actions.downgrade_ftl()`.
                                        # None can be specified if there's no downgrader available.
    sha1: str                           # SHA1 hash value of FTLGame.exe, in lowercase

@dataclass(frozen=True)
class HyperspaceInfo:                   # A signature of Hyperspace.dll
    name: str                           # The version displayed in the installer app
    outdated: bool                      # Whether it's outdated to run the latest Multiverse
    latest: bool                        # Whether it's the latest version to be used for installing or updating HS.
                                        # There should be EXACTLY one entry that has `latest=True`. Set others as False.
    sha1: str                           # SHA1 hash value of Hyperspace.dll, in lowercase
    url: str                            # URL to the Hyperspace release
    filename: str                       # Filename of the Hyperspace release

@dataclass(frozen=True)
class Mod:                              # A mod
    id: str                             # ID (slug) of the mod.
    modname: str                        # Original mod name. Each localized mod(the same mods) must have the same modname, defferent id.
    download_targets: dict[str, str]    # List of mod files in {url: filename} form
    version: str                        # Version string
    locale: str                         # Locale code
    metadata_url: Optional[str]         # URL to the metadata.xml
    compatible_mv_locale: list[str]     # Multiverse locale to be used with. If empty, it's compatible with all locales. Locale specific version has higher priority than empty one if both have the same modname and are compatible with current locale.
    dependent_modnames: list[str]       # Dependencies of the mod (list of modname). You cannot install the mod without these mods. If empty, it has no dependencies.
    priority: int                       # Installtion priority in ascending order. Mainmod is 0, and each official addons are 100, 200, 300, ...

########## Signatures

class FtlExecutableType(Enum):
    STEAM_WINDOWS_1_6_14 = FtlExecutableInfo(
        name='Steam, version 1.6.14 (latest)',
        downgraded=False,
        downgrader='steam',
        sha1='c58e5283b2c1996fa36158265423f8c94f3a8954',
    )
    STEAM_WINDOWS_1_6_9 = FtlExecutableInfo(
        name='Steam, version 1.6.9 (downgraded)',
        downgraded=True,
        downgrader=None,
        sha1='8f23c8e704f793fb108d12c489644b5393c8bc2d',
    )
    GOG_WINDOWS_1_6_13B = FtlExecutableInfo(
        name='GOG, version 1.6.13b (latest)',
        downgraded=False,
        downgrader=None,
        sha1='0db27c60ae7986cbeb19ffda3eee6470daf984db',
    )
    GOG_WINDOWS_1_6_9 = FtlExecutableInfo(
        name='GOG, version 1.6.9 (downgraded)',
        downgraded=True,
        downgrader=None,
        sha1='609ef1bd507097e2b41bd57b9e81e7f2061aadc2',
    )
    HUMBLE_BUNDLE_WINDOWS_1_6_12 = FtlExecutableInfo(
        name='Humble Bundle, version 1.6.12 (latest)',
        downgraded=False,
        downgrader=None,
        sha1='b4eae8d8690c8bc7b80def6e8224fb17d34a5083',
    )
    EPIC_WINDOWS_1_6_12 = FtlExecutableInfo(
        name='Epic Games Store, version 1.6.12 (latest)',
        downgraded=False,
        downgrader='epic',
        sha1='7b8c4d0657e16edc98b9978bd9a9f851a613573a',
    )
    ORIGIN_WINDOWS_1_6_12 = FtlExecutableInfo(
        name='Origin, version 1.6.12 (latest)',
        downgraded=False,
        downgrader='origin',
        sha1='16c2d7936e9bb5c40672ad7593b5285860b2a5db',
    )


class HyperspaceType(Enum):
    HS_1_2_3 = HyperspaceInfo(
        name='HS-1.2.3 6a7ef87',
        outdated=True,
        latest=False,
        sha1='99b7fae6ef2df05ad6e9370e7d04987fdaa101ff',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.2.3/FTL.Hyperspace.1.2.3.zip',
        filename='FTL.Hyperspace.1.2.3.zip'
    )
    HS_1_3_0 = HyperspaceInfo(
        name='HS-1.3.0 1705ea5',
        outdated=True,
        latest=False,
        sha1='558a7de6d841a7b26bf368b252d12ecd15ff09c5',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.3.0/FTL.Hyperspace.1.3.0.zip',
        filename='FTL.Hyperspace.1.3.0.zip'
    )
    HS_1_3_1 = HyperspaceInfo(
        name='HS-1.3.1 2a6c7eb',
        outdated=True,
        latest=False,
        sha1='85ecd040c98d703699a84384d77ef8a890872161',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.3.1/FTL.Hyperspace.1.3.1.zip',
        filename='FTL.Hyperspace.1.3.1.zip'
    )
    HS_1_3_2 = HyperspaceInfo(
        name='HS-1.3.2 56a6aec',
        outdated=True,
        latest=False,
        sha1='fd7218b3b16802066e450a23fe48ba9daf43d08b',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.3.2/FTL.Hyperspace.1.3.2.zip',
        filename='FTL.Hyperspace.1.3.2.zip'
    )
    HS_1_3_3 = HyperspaceInfo(
        name='HS-1.3.3 9afe729',
        outdated=True,
        latest=False,
        sha1='8e12408b6a308c98ce362fbf2576f21c0280948c',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.3.3/FTL.Hyperspace.1.3.3.zip',
        filename='FTL.Hyperspace.1.3.3.zip'
    )
    HS_1_4_0 = HyperspaceInfo(
        name='HS-1.4.0 34add76',
        outdated=True,
        latest=False,
        sha1='5540277b0513e68d4348b253e75f09c4b6d47f26',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.4.0/FTL.Hyperspace.1.4.0.zip',
        filename='FTL.Hyperspace.1.4.0.zip'
    )
    HS_1_5_0 = HyperspaceInfo(
        name='HS-1.5.0 9afe729',
        outdated=True,
        latest=False,
        sha1='4fad1eda06706479c819dd2310ae286f90dd4b74',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.5.0/FTL.Hyperspace.1.5.0.zip',
        filename='FTL.Hyperspace.1.5.0.zip'
    )
    HS_1_7_1 = HyperspaceInfo(
        name='HS-1.7.1 6099b55',
        outdated=True,
        latest=False,
        sha1='0e9023129177c46c43ba8db35279bf8218fae313',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.7.1/FTL.Hyperspace.1.7.1.zip',
        filename='FTL.Hyperspace.1.7.1.zip'
    )
    HS_1_8_0 = HyperspaceInfo(
        name='HS-1.8.0 b1a5714',
        outdated=True,
        latest=False,
        sha1='62f3312ac08ffae7ade2e289666f61e6abdc0061',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.8.0/FTL.Hyperspace.1.8.0.zip',
        filename='FTL.Hyperspace.1.8.0.zip'
    )
    HS_1_9_0 = HyperspaceInfo(
        name='HS-1.9.0 b9eeb4a',
        outdated=True,
        latest=False,
        sha1='acb0c32b82019de6134e3aff8a3052e599fbdeb8',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.9.0/FTL.Hyperspace.1.9.0.zip',
        filename='FTL.Hyperspace.1.9.0.zip'
    )
    HS_1_10_2 = HyperspaceInfo(
        name='HS-1.10.2 bd32359',
        outdated=True,
        latest=False,
        sha1='9029758e467bc7b2a019a516dd62e16afa24549d',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.10.2/FTL.Hyperspace.1.10.2.zip',
        filename='FTL.Hyperspace.1.10.2.zip'
    )
    HS_1_11_0 = HyperspaceInfo(
        name='HS-1.11.0 9c6df50',
        outdated=True,
        latest=False,
        sha1='cca58c4aa72737f7daf75b6c86067ca5945c3eca',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.11.0/FTL.Hyperspace.1.11.0.zip',
        filename='FTL.Hyperspace.1.11.0.zip'
    )
    HS_1_11_1 = HyperspaceInfo(
        name='HS-1.11.1 f374340',
        outdated=True,
        latest=False,
        sha1='5497a1d1274ecea94e50b330ba4d0a6c38c4a76f',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.11.1/FTL.Hyperspace.1.11.1.zip',
        filename='FTL.Hyperspace.1.11.1.zip'
    )
    HS_1_11_2 = HyperspaceInfo(
        name='HS-1.11.2 0c3a7b1',
        outdated=True,
        latest=False,
        sha1='946f89944bd805ffab60b6c19c579ce2deb429d7',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.11.2/FTL.Hyperspace.1.11.2.zip',
        filename='FTL.Hyperspace.1.11.2.zip'
    )
    HS_1_12_0 = HyperspaceInfo(
        name='HS-1.12.0 8fbfc43',
        outdated=True,
        latest=False,
        sha1='67119b8017afcebce031f60a8b3ac924106492cb',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.12.0/FTL.Hyperspace.1.12.0.zip',
        filename='FTL.Hyperspace.1.12.0.zip'
    )
    HS_1_13_0 = HyperspaceInfo(
        name='HS-1.13.0 89c448a',
        outdated=True,
        latest=False,
        sha1='fedc710efcfc0f8761550ce3259d57be1e5cdcaa',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.13.0/FTL.Hyperspace.1.13.0.zip',
        filename='FTL.Hyperspace.1.13.0.zip'
    )
    HS_1_13_1 = HyperspaceInfo(
        name='HS-1.13.1 58c7f4b',
        outdated=True,
        latest=False,
        sha1='e5101872deed78c1f5462d666fd4aa727cb5b5c6',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.13.1/FTL.Hyperspace.1.13.1.zip',
        filename='FTL.Hyperspace.1.13.1.zip'
    )
    HS_1_13_3 = HyperspaceInfo(
        name='HS-1.13.3 53b8334',
        outdated=True,
        latest=False,
        sha1='0c5f544dae9ecbc693b83e85a6a86897a3bf1543',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.13.3/FTL.Hyperspace.1.13.3.zip',
        filename='FTL.Hyperspace.1.13.3.zip'
    )
    HS_1_13_4 = HyperspaceInfo(
        name='HS-1.13.4 79da3a4',
        outdated=True,
        latest=False,
        sha1='8dec29c9f88770d246cffd18264cebfd16f153ed',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.13.4/FTL.Hyperspace.1.13.4.zip',
        filename='FTL.Hyperspace.1.13.4.zip'
    )
    HS_1_14_2 = HyperspaceInfo(
        name='HS-1.14.2 1237d68',
        outdated=True,
        latest=False,
        sha1='6a0b04d06a59ff8bee6b8f423247d96eb4d17a6d',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.14.2/FTL.Hyperspace.1.14.2.zip',
        filename='FTL.Hyperspace.1.14.2.zip'
    )
    HS_1_15_0 = HyperspaceInfo(
        name='HS-1.15.0 09a44d5',
        outdated=True,
        latest=False,
        sha1='a9215f154421788c007821a2cca3ad00b90be671',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.15.0/FTL.Hyperspace.1.15.0.zip',
        filename='FTL.Hyperspace.1.15.0.zip'
    )
    HS_1_15_1 = HyperspaceInfo(
        name='HS-1.15.1 2f6256a',
        outdated=True,
        latest=False,
        sha1='6fc7d6e7ad15e0af0ef3161097c8e17dbe9b73b1',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.15.1/FTL.Hyperspace.1.15.1.zip',
        filename='FTL.Hyperspace.1.15.1.zip'
    )
    HS_1_17_0 = HyperspaceInfo(
        name='HS-1.17.0 15942e4',
        outdated=True,
        latest=False,
        sha1='5fd0f28540c31cdffdac6094fcd460fd8de188b5',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.17.0/FTL.Hyperspace.1.17.0.zip',
        filename='FTL.Hyperspace.1.17.0.zip'
    )
    HS_1_17_1 = HyperspaceInfo(
        name='HS-1.17.1 ffc959e',
        outdated=True,
        latest=False,
        sha1='57a58be2930236a5e5152509bf0d21307116cdb8',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.17.1/FTL.Hyperspace.1.17.1.zip',
        filename='FTL.Hyperspace.1.17.1.zip'
    )
    HS_1_18_1 = HyperspaceInfo(
        name='HS-1.18.1 fd6911a',
        outdated=True,
        latest=False,
        sha1='21d3e20e03e925db536208a975dac2aa58d4a181',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.18.1/FTL.Hyperspace.1.18.1.zip',
        filename='FTL.Hyperspace.1.18.1.zip'
    )
    HS_1_19_0 = HyperspaceInfo(
        name='HS-1.19.0 b52c257',
        outdated=False,
        latest=True,
        sha1='0633427e0a8760fd4219ca74dee8e4ef446f9127',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.19.0/FTL.Hyperspace.1.19.0.zip',
        filename='FTL.Hyperspace.1.19.0.zip'
    )


# SHA1 hash value of unmodded ftl.dat files
DAT_VANILLA_SHA1 = [
    'a0ecc84f16302b8851eff98ab3e01e2f376152d7', # Steam 1.6.14
    '2b81ef942c56fd4025ba11eecfd8ac6100de206f', # GOG 1.6.13b
    'b7c923866726607d172461454b8904b6d3dfb811', # GOG 1.6.9
    '42270f1e2ab35b4a69fb6c5141a87196a43f9e63', # Humble Bundle 1.6.12
]

# Default locations to search for FTL installation
FIXED_PATHS = [
    # Steam
    r'C:\Program Files\Steam\steamapps\common\FTL Faster Than Light',
    r'C:\Program Files (x86)\Steam\steamapps\common\FTL Faster Than Light',

    # Humble Bundle
    r'C:\Program Files (x86)\FTL',

    # GOG
    r'C:\Program Files (x86)\GOG Galaxy\Games\FTL Advanced Edition',

    # Epic
    r'C:\Program Files\Epic Games\FasterThanLight',
]

########## Downgraders

DOWNGRADERS = {
    'epic': (
        'https://drive.google.com/uc?id=1wM4Lb1ADy3PHay5sNuWpQOTnWbpIOGQ1&confirm=t',
        'Epic Games Downgrade Patcher (1.6.12 to 1.6.9).zip'
    ),
    'origin': (
        'https://drive.google.com/uc?id=1GTxiidyp0o5D1HBMrT0XprstVmPwvuqo&confirm=t',
        'Origin Downgrade Patcher (1.6.12 to 1.6.9).zip'
    )
}

########## ftlman (We have migrated from Slipstream Mod Manager)

SMM_URL = 'https://github.com/afishhh/ftlman/releases/latest/download/ftlman-x86_64-pc-windows-gnu.zip'
SMM_FILENAME = 'ftlman-x86_64-pc-windows-gnu.zip' # The file name of the archive
SMM_ROOT_DIR = 'ftlman' # The root directory of ftlman in the archive

########## Mods

# The English main mod
# MV_ENGLISH_MAINMOD = Mod(
#     id='FTL-Multiverse/en',
#     download_targets={
#         'https://drive.google.com/uc?id=1U94fcFtdJQirHvrH4G9gGehA02Q-GHUU&confirm=t':
#             'Multiverse 5.3 - Assets (Patch First).zip',
#         'https://drive.google.com/uc?id=17XDwphfmFIWxHy5ReCVR64Lo5XTb1GIL&confirm=t':
#             'Multiverse 5.3.1 - Data (hotfix for extreme).zip'
#     },
#     version='5.3.1',
#     locale='en',
#     metadata_url='',
#     compatible_mv_locale=['en']
# )

RELEASE_EXPIRE_DURATION = 60 * 60 * 24 # Updated every day
MAINMODS_TRANSLATION_RELEASE = 'https://api.github.com/repos/ftl-mv-translation/ftl-mv-translation/releases/latest'#mv, priority=0
ADDONS_TRANSLATION_RELEASE = [
    'https://api.github.com/repos/ftl-mv-translation/trc/releases/latest', #trc, priority=100
    'https://api.github.com/repos/ftl-mv-translation/fishier-than-light/releases/latest', #fishier-than-light, priority=200
    'https://api.github.com/repos/ftl-mv-translation/forgotten-races/releases/latest', #fr, priority=300
    'https://api.github.com/repos/ftl-mv-translation/forgotten-diamonds/releases/latest', #fr-diamonds, priority=400
    'https://api.github.com/repos/ftl-mv-translation/outer-expansion/releases/latest', #OE, priority=500
    'https://api.github.com/repos/ftl-mv-translation/forgemaster/releases/latest', #forgemaster, priority=600
    'https://api.github.com/repos/ftl-mv-translation/piracy-is-poggers/releases/latest', #PiP, priority=700
    'https://api.github.com/repos/ftl-mv-translation/RAD/releases/latest', #R&D, priority=800
    'https://api.github.com/repos/ftl-mv-translation/darkest-desire/releases/latest', #DD, priority=900
]

TRANSLATION_RELEASE_DEPENDENCIES = {
    'Forgemaster': ['Fusion'],
    'Forgotten-Races': ['The-Renegade-Collection', 'Fusion'],
    'Forgotten-Diamonds': ['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
    'Outer-Expansion': ['TOEPatchLast']
}

LIBRARY_MODS = [
    'Fusion', 'TOEPatchLast'
]

class FixedAddonsList(Enum):
    #mv, priority=0
    GenGibsMV = Mod(
        id='GenGibsMV',
        modname='GenGibsMV',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1JFSm0418yTVRloTiQLFM5E7Wvwu6w4Gi&export=download&confirm=xxx':
                'MV Addon GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsMV.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=1
    )
    GenGibsMV_RU = Mod(
        id='GenGibsMV_RU',
        modname='GenGibsMV',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1-N3EAFL_E61NFs2qLFskghvKvThZqaYY&export=download&confirm=xxx':
                'MV Addon GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsMV_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1
    )
    #trc, priority=100
    GenGibsTRC = Mod(
        id='GenGibsTRC',
        modname='GenGibsTRC',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1BoYFKqPQQJ5CE9kSbufSKx9jWdyeiYRl&export=download&confirm=xxx':
                'MV TRC GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsTRC.xml',
        compatible_mv_locale=[],
        dependent_modnames=['The-Renegade-Collection'],
        priority=101
    )
    GenGibsTRC_RU = Mod(
        id='GenGibsTRC_RU',
        modname='GenGibsTRC',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1BoYFKqPQQJ5CE9kSbufSKx9jWdyeiYRl&export=download&confirm=xxx':
                'MV TRC GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsTRC_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['The-Renegade-Collection'],
        priority=101
    )
    Fusion = Mod(
        id='Fusion',
        modname='Fusion',
        download_targets={
            'https://github.com/MV-Fusion-Team/FTL-Multiverse-Fusion/releases/download/v0.1.4/Fusion.zip':
                'Fusion.zip'
        },
        version='0.1.4',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=103
    )
    #Fishing, priority=200
    #fr, priority=300
    #fr-diamonds, priority=400
    
    JudgeBlueOptionsRU = Mod(
        id='JudgeBlueOptionsRU',
        modname='JudgeBlueOptions',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1-88OSmVafL30rYGhRgLB13AEL_v_xems&export=download&confirm=xxx':
                'Multiverse.-.Judge.Blue.Options.1.4.zip'
        },
        version='1.4',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/JBO_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=401
    )
    
    #OE, priority=500

    GenGibsFR = Mod(
        id='GenGibsFR',
        modname='GenGibsFR',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1N3OvTEnuF2SbzDWAZEbI2qGBKe1JQGCZ&export=download&confirm=xxx':
                'Forgotten Gibs 1.5.1.zip'
        },
        version='1.5.1',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsFR.xml',
        compatible_mv_locale=[],
        dependent_modnames=['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
        priority=501
    )
    GenGibsFR_RU = Mod(
        id='GenGibsFR_RU',
        modname='GenGibsFR',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1N3OvTEnuF2SbzDWAZEbI2qGBKe1JQGCZ&export=download&confirm=xxx':
                'Forgotten Gibs 1.5.1.zip'
        },
        version='1.5.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/GenGibsFR_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
        priority=501
    )
    #forgemaster, priority=600
    #PiP, priority=700
    #R&D, priority=800
    #DD, priority=900

    NoHardModeScrap = Mod(
        id='NoHardModeScrap',
        modname='NoHardModeScrap',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-W5m78H5QESr9rvNpCJ4A11Q1sRKefgU&export=download&confirm=xxx':
                'No Hard Mode Scrap Penalty 3.0.zip'
        },
        version='3.0',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/NoHardModeScrap.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=5003
    )
    NoHardModeScrapRU = Mod(
        id='NoHardModeScrapRU',
        modname='NoHardModeScrap',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-W5m78H5QESr9rvNpCJ4A11Q1sRKefgU&export=download&confirm=xxx':
                'No Hard Mode Scrap Penalty 3.0.zip'
        },
        version='3.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/NoHardModeScrapRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5003
    )
    LizzardAchRU = Mod(
        id='LizzardAchRU',
        modname='LizzardAch',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1hDDoNtNaGCypA1-xib6Xai2vQd3aw7r2&export=download&confirm=xxx':
                'Lizzard achievements.zip'
        },
        version='-0.9.9',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/LizzardAchRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5004
    )
    LizzardAchDE = Mod(
        id='LizzardAchDE',
        modname='LizzardAch',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1hDDoNtNaGCypA1-xib6Xai2vQd3aw7r2&export=download&confirm=xxx':
                'Lizzard achievements.zip'
        },
        version='-0.9.9',
        locale='de',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/LizzardAchEN.xml',
        compatible_mv_locale=['de'],
        dependent_modnames=[],
        priority=5004
    )
    VanUI = Mod(
        id='VanUI',
        modname='VanUI',
        download_targets={
            'https://drive.usercontent.google.com/u/0/uc?id=1-RSAqQI-2tBxDYy5SGtoctIis_vYD8KO&export=download&confirm=xxx':
                'Multiverse - VanUI 4.0.zip'
        },
        version='4.0',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/VanillaUI.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=5006
    )
    VanUI_RU = Mod(
        id='VanUI_RU',
        modname='VanUI',
        download_targets={
            'https://drive.usercontent.google.com/u/0/uc?id=1-RSAqQI-2tBxDYy5SGtoctIis_vYD8KO&export=download&confirm=xxx':
                'Multiverse - VanUI 4.0.zip'
        },
        version='4.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/VanUI_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5006
    )
    VanUI_KO = Mod(
        id='VanUI_KO',
        modname='VanUI',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-RT9eTadViQLY4Au8-3L6rTWZT3u-0l7&export=download&confirm=xxx':
                'Multiverse - VanUI 4.0 (Korean).zip'
        },
        version='4.0',
        locale='ko',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/VanillaUI.xml',
        compatible_mv_locale=['ko'],
        dependent_modnames=[],
        priority=5006
    )
    ItBHUD_RU = Mod(
        id='ItBHUD_RU',
        modname='ItBHUD',
        download_targets={
            'https://drive.usercontent.google.com/u/0/uc?id=1-VzupAbhge90ULVHjN69dd85Cpu5hReN&export=download&confirm=xxx':
                'MV Into The Breach HUD.ftl'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/ItBHUD_RU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5007
    )
    MoreManSysRU = Mod(
        id='MoreManSysRU',
        modname='MoreManSys',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-3-MHlG_Xn_Pufhj9zmuxamFfbltz6f6&export=download&confirm=xxx':
                'MoreMannableSystems_v1.4.zip'
        },
        version='1.4',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/MoreManSysRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5008
    )
    BoonSelectorRU = Mod(
        id='BoonSelectorRU',
        modname='BoonSelector',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1--aXLu18JKrncsbbUeZ3HSm2COsQc8Fv&export=download&confirm=xxx':
                'Multiverse.Judge.Boon.Selector.ftl'
        },
        version='1.4.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/BoonSelectorRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5009
    )
    HereBeMarkersRU = Mod(
        id='HereBeMarkersRU',
        modname='HereBeMarkers',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-4sV0eYHSx1zP551s3xkB0JO5wGVCQGk&export=download&confirm=xxx':
                'Here be Markers 3.1.zip'
        },
        version='3.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/HereBeMarkersRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5010
    )
    HereBeMarkersPlusRU = Mod(
        id='HereBeMarkersPlusRU',
        modname='HereBeMarkersPlus',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-MpUpRMbnQkBU1-c_OGf933UPv0ThK4d&export=download&confirm=xxx':
                'Here Be Markers Plus 3.1.zip'
        },
        version='3.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/addon_metadata/HereBeMarkersPlusRU.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=5011
    )
    TOEPatchLast = Mod(
        id='TOEPatchLast',
        modname='TOEPatchLast',
        download_targets={
            'https://github.com/arcburnergit/FTL-Outer-Expansion/releases/download/v7.1.2/FTL-Outer-Expansion-PATCH_AFTER_ALL_OTHER_ADDONS.ftl':
                'FTL-Outer-Expansion-PATCH_AFTER_ALL_OTHER_ADDONS.ftl'
        },
        version='1.0.0',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=5021
    )