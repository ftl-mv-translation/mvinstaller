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


class HyperspaceType(Enum):
    HS_1_2_3 = HyperspaceInfo(
        name='HS-1.2.3 6a7ef87',
        outdated=False,
        latest=False,
        sha1='99b7fae6ef2df05ad6e9370e7d04987fdaa101ff',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.2.3/FTL.Hyperspace.1.2.3.zip',
        filename='FTL.Hyperspace.1.2.3.zip'
    )
    HS_1_3_0 = HyperspaceInfo(
        name='HS-1.3.0 1705ea5',
        outdated=False,
        latest=True,
        sha1='558a7de6d841a7b26bf368b252d12ecd15ff09c5',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.3.0/FTL.Hyperspace.1.3.0.zip',
        filename='FTL.Hyperspace.1.3.0.zip'
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
        'https://drive.google.com/uc?id=1EDY0tX4N-w-bmJ5Qf65GAZ9h5iRiR6ny&confirm=t':
            'Multiverse 5.3 - Data.zip'
    },
    version='5.3',
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

