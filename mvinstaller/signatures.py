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
class MainMod:                          # A main Multiverse mod
    download_targets: dict[str, str]    # List of mod files in {url: filename} form
    version: str                        # Version string
    locale: str                         # Locale code
    commitid: Optional[str]             # Commit ID (useful for distinguishing versions between nightly translation)

@dataclass(frozen=True)
class Addon:                            # An addon mod
    download_targets: dict[str, str]    # List of mod files in {url: filename} form
    metadata_name: str                  # A path to the metadata.xml in addon_metadata directory
                                        # with 'addon_metadata/' and '.xml' stripped out
    custom_metadata: bool               # Controls whether metadata.xml should be updated by the fetch_metadata script.
                                        # Set to True if it should NOT update the metadata.
    locale: Optional[list[str]]         # Available locales. If it is None, every locale of MV can use it.

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
        outdated=False,
        latest=False,
        sha1='4fad1eda06706479c819dd2310ae286f90dd4b74',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.5.0/FTL.Hyperspace.1.5.0.zip',
        filename='FTL.Hyperspace.1.5.0.zip'
    )
    HS_1_7_1 = HyperspaceInfo(
        name='HS-1.7.1 6099b55',
        outdated=False,
        latest=True,
        sha1='0e9023129177c46c43ba8db35279bf8218fae313',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.7.1/FTL.Hyperspace.1.7.1.zip',
        filename='FTL.Hyperspace.1.7.1.zip'
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

########## Slipstream Mod Manager

# A proper distribution comes from Sourceforge (https://sourceforge.net/projects/slipstreammodmanager/).
# Here the Windows distribution for 1.9.1 has been copied the to the ftlmv-weblate-bot GDrive
# (the one that houses translated MV packages), as it's a bit tricky to implement a programmatic downloader for SF.
SMM_URL = 'https://drive.google.com/uc?id=194uP5DHmI7bU56soStbv4MfRat2xpXiu&confirm=t'
SMM_FILENAME = 'SlipstreamModManager_1.9.1-Win.zip' # The file name of the archive
SMM_ROOT_DIR = 'SlipstreamModManager_1.9.1-Win' # The root directory of SMM in the archive

########## Mods

# The English main mod
MV_ENGLISH_MAINMOD = MainMod(
    download_targets={
        'https://drive.google.com/uc?id=1U94fcFtdJQirHvrH4G9gGehA02Q-GHUU&confirm=t':
            'Multiverse 5.3 - Assets (Patch First).zip',
        'https://drive.google.com/uc?id=17XDwphfmFIWxHy5ReCVR64Lo5XTb1GIL&confirm=t':
            'Multiverse 5.3.1 - Data (hotfix for extreme).zip'
    },
    version='5.3.1',
    locale='en',
    commitid=None
)

# The listfile for the nightly main mod translations
LISTFILE_EXPIRE_DURATION = 60 * 60 * 24 # Updated every day
LISTFILE_URL = 'https://raw.githubusercontent.com/ftl-mv-translation/ftl-mv-translation/installer-metadata/listfile'

class AddonsList(Enum):
    GenGibs = Addon(
        download_targets={
            'https://drive.google.com/uc?id=11YlBrNHCpyIEwX41IEj2RjWP6haH3--4&confirm=t':
                'MV Addon GenGibs v1.2.0.ftl'
        },
        metadata_name='GenGibs',
        custom_metadata=False,
        locale=None
    )
    TRC_ko = Addon(
        download_targets={
            'https://drive.google.com/uc?id=15kNTm-_CaHz3XaNCRPSwBAxOvkcvP7qb&confirm=t':
                'Multiverse - TRC 1.3 - Korean.ftl'
        },
        metadata_name='TRC_ko',
        custom_metadata=True,
        locale=['ko']
    )

