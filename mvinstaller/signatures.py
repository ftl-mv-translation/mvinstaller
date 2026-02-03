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
        outdated=True,
        latest=False,
        sha1='0633427e0a8760fd4219ca74dee8e4ef446f9127',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.19.0/FTL.Hyperspace.1.19.0.zip',
        filename='FTL.Hyperspace.1.19.0.zip'
    )
    HS_1_19_1 = HyperspaceInfo(
        name='HS-1.19.1 cb0fe57',
        outdated=True,
        latest=False,
        sha1='2b394b1b8c4e81a1a1f287b8c8adeba24e3f5003',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.19.1/FTL.Hyperspace.1.19.1.zip',
        filename='FTL.Hyperspace.1.19.1.zip'
    )
    HS_1_20_0 = HyperspaceInfo(
        name='HS-1.20.0 2540d80',
        outdated=True,
        latest=False,
        sha1='2462b664fe6ad17ed1d107e983dbc469e81e9acd',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.20.0/FTL.Hyperspace.1.20.0.zip',
        filename='FTL.Hyperspace.1.20.0.zip'
    )
    HS_1_21_1 = HyperspaceInfo(
        name='HS-1.21.1 e4a5c18',
        outdated=False,
        latest=True,
        #sha1='f0bcf23ec6ba018d53d2c88933a0b5cdde653c25',
        sha1='fbdc72256f7942ad067a0a16e11ac665e4bd5c75',
        url='https://github.com/FTL-Hyperspace/FTL-Hyperspace/releases/download/v1.21.1/FTL.Hyperspace.1.21.1.zip',
        filename='FTL.Hyperspace.1.21.1.zip'
    )

# SHA1 hash value of unmodded ftl.dat files
DAT_VANILLA_SHA1 = [
    #'', # Steam 1.6.22
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
    'https://api.github.com/repos/ftl-mv-translation/darkest-desire/releases/latest', #DD, priority=600
    'https://api.github.com/repos/ftl-mv-translation/expanded-multiverse/releases/latest', #EMV, priority=700
    'https://api.github.com/repos/ftl-mv-translation/forgemaster/releases/latest', #forgemaster, priority=800
    'https://api.github.com/repos/ftl-mv-translation/piracy-is-poggers/releases/latest', #PiP, priority=900
    'https://api.github.com/repos/ftl-mv-translation/RAD/releases/latest', #R&D, priority=1000
    'https://api.github.com/repos/ftl-mv-translation/lilys-beam-emporium/releases/latest', #LBE, priority=1100
    'https://api.github.com/repos/ftl-mv-translation/old-guard/releases/latest', #OG, priority=1200
    'https://api.github.com/repos/ftl-mv-translation/Eschaton-Genesis/releases/latest', #EG, priority=1300
    'https://api.github.com/repos/ftl-mv-translation/lilys-innovations/releases/latest', #LI, priority=1400
]

TRANSLATION_RELEASE_DEPENDENCIES = {
    'Forgemaster': ['Fusion'],
    'Forgotten-Races': ['The-Renegade-Collection', 'Fusion'],
    'Forgotten-Diamonds': ['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
    'Outer-Expansion': ['TOEPatchLast'],
    'Darkest-Desire': ['DDPatchLast'],
    'Old-Guard': ['OGPatchLast'],
    'Expanded-Multiverse': ['Fusion'],
    'Eschaton-Genesis': ['Fusion']
}

LIBRARY_MODS = [
    'Fusion', 'TOEPatchLast', 'DDPatchLast', 'VertexUtil', 'Brightness_Particle_System', 'Lightweight_Lua', 'OGPatchLast'
]

class FixedAddonsList(Enum):
    #mv, priority=0  
    #trc, priority=100
    Fusion = Mod(
        id='Fusion',
        modname='Fusion',
        download_targets={
            'https://github.com/MV-Fusion-Team/FTL-Multiverse-Fusion/releases/download/v0.1.6/Fusion.zip':
                'Fusion.zip'
        },
        version='0.1.6',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=101
    )
    VertexUtil = Mod(
        id='VertexUtil',
        modname='VertexUtil',
        download_targets={
            'https://github.com/ChronoVortex/FTL-HS-Vertex/releases/download/v6.3/Vertex-Util.ftl':
                'VertexUtil.ftl'
        },
        version='6.3',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=102
    )
    Brightness_Particle_System = Mod(
        id='Brightness_Particle_System',
        modname='Brightness_Particle_System',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1rHHtawmH0IoHnab-W1GaHrtKnhaHD2zq&export=download&confirm=xxx':
                'Brightness Particles 1.4.1.zip'
        },
        version='1.4.1',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=103
    )
    Lightweight_Lua = Mod(
        id='Lightweight_Lua',
        modname='Lightweight_Lua',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1jIEeIo4igYl5C3TaIEhizQ-y1FFnH_KX&export=download&confirm=xxx':
                'Lightweight_Lua.zip'
        },
        version='6.3',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=104
    )
    #Fishing, priority=200
    #fr, priority=300
    #fr-diamonds, priority=400
    #OE, priority=500
    #DD, priority=600
    #EMV, priority=700
    #FM, priority=800
    #PiP, priority=900
    HektarBundleRU = Mod(
        id='HektarBundleRU',
        modname='HektarBundle',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1I5r-jC1N-fRVYA9efuMIfoQ61_3YMez7&export=download&confirm=xxx':
                'FTL.Multiverse.-.Hektar.Bundle.zip'
        },
        version='0.1.7',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=901
    )
    #R&D, priority=1000
    #LBE, priority=1100
    #OG, priority=1200
    Eschaton_GenesisRU = Mod(
        id='Eschaton_GenesisRU',
        modname='Eschaton_Genesis',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1qlQWUcIeltDesnYfjgnI-WFMgc_0kCr7&export=download&confirm=xxx':
                'ESCHATON_GENESIS.zip'
        },
        version='0.2',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1201
    )
    EternalVerseRU = Mod(
        id='EternalVerseRU',
        modname='EternalVerse',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1zWLo-muGpaiHyyoo_PkImEU9Qi7tFAYn&export=download&confirm=xxx':
                'EternalVerse.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['VertexUtil'],
        priority=1202
    )
    UniversalThreatsRU = Mod(
        id='UniversalThreatsRU',
        modname='UniversalThreats',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1Ujp1DiQ2SIZj6Nwe3FH5bu51Xz7gVBoa&export=download&confirm=xxx':
                'Universal_Threats.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1203
    )
    TNE_RU = Mod(
        id='TNE_RU',
        modname='TNE',
        download_targets={
            'https://drive.usercontent.google.com/download?id=18niicFjYarSqXHXqzHcaaZlzcCWNN0Ps&export=download&confirm=xxx':
                'TNE_v1.25c.ftl'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1210
    )
    TNE_ZH_HANS = Mod(
        id='TNE_ZH_HANS',
        modname='TNE',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1WdLhAp04Hz2Ny3H7fFE4yHO7Y4l7HdCb&export=download&confirm=xxx':
                'TNE_v1.25c.ftl'
        },
        version='1.0',
        locale='zh_Hans',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['zh_Hans'],
        dependent_modnames=[],
        priority=1210
    )
    GenGibsMV = Mod(
        id='GenGibsMV',
        modname='GenGibsMV',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1JFSm0418yTVRloTiQLFM5E7Wvwu6w4Gi&export=download&confirm=xxx':
                'MV Addon GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=1254
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1254
    )
    GenGibsMV_FR = Mod(
        id='GenGibsMV_FR',
        modname='GenGibsMV',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1-N3EAFL_E61NFs2qLFskghvKvThZqaYY&export=download&confirm=xxx':
                'MV Addon GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=[],
        priority=1254
    )
    GenGibsTRC = Mod(
        id='GenGibsTRC',
        modname='GenGibsTRC',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1BoYFKqPQQJ5CE9kSbufSKx9jWdyeiYRl&export=download&confirm=xxx':
                'MV TRC GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=['The-Renegade-Collection'],
        priority=1255
    )
    GenGibsTRC_FR = Mod(
        id='GenGibsTRC_FR',
        modname='GenGibsTRC',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1BoYFKqPQQJ5CE9kSbufSKx9jWdyeiYRl&export=download&confirm=xxx':
                'MV TRC GenGibs v1.4.2.ftl'
        },
        version='1.4.2',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=['The-Renegade-Collection'],
        priority=1255
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['The-Renegade-Collection'],
        priority=1255
    )
    GenGibsFR = Mod(
        id='GenGibsFR',
        modname='GenGibsFR',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1N3OvTEnuF2SbzDWAZEbI2qGBKe1JQGCZ&export=download&confirm=xxx':
                'Forgotten Gibs 1.5.1.zip'
        },
        version='1.5.1',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
        priority=1256
    )
    GenGibsFR_FR = Mod(
        id='GenGibsFR_FR',
        modname='GenGibsFR',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1N3OvTEnuF2SbzDWAZEbI2qGBKe1JQGCZ&export=download&confirm=xxx':
                'Forgotten Gibs 1.5.1.zip'
        },
        version='1.5.1',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
        priority=1256
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['The-Renegade-Collection', 'Fusion', 'Forgotten-Races'],
        priority=1256
    )
    GenGibsDD = Mod(
        id='GenGibsDD',
        modname='GenGibsDD',
        download_targets={
            'https://drive.usercontent.google.com/download?id=11w2PRVW0BRAogf-k-_eKL7gBTFJ0i_E_&export=download&confirm=xxx':
                'DD Addon GenGibs.zip'
        },
        version='1.0',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=['Darkest-Desire'],
        priority=1257
    )
    GenGibsDD_FR = Mod(
        id='GenGibsDD_FR',
        modname='GenGibsDD',
        download_targets={
            'https://drive.usercontent.google.com/download?id=11w2PRVW0BRAogf-k-_eKL7gBTFJ0i_E_&export=download&confirm=xxx':
                'DD Addon GenGibs.zip'
        },
        version='1.0',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=['Darkest-Desire'],
        priority=1257
    )
    GenGibsDD_RU = Mod(
        id='GenGibsDD_RU',
        modname='GenGibsDD',
        download_targets={
            'https://drive.usercontent.google.com/download?id=11w2PRVW0BRAogf-k-_eKL7gBTFJ0i_E_&export=download&confirm=xxx':
                'DD Addon GenGibs.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['Darkest-Desire'],
        priority=1257
    )
    ExtraCapacity = Mod(
        id='ExtraCapacity',
        modname='ExtraCapacity',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1d-GXx7NiT1KfZh57HYVRjNvT-7lNLuzH&export=download&confirm=xxx':
                'lilys-extra-capacity.ftl'
        },
        version='1.0',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=1349
    )
    ExtraCapacityRU = Mod(
        id='ExtraCapacityRU',
        modname='ExtraCapacity',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1d-GXx7NiT1KfZh57HYVRjNvT-7lNLuzH&export=download&confirm=xxx':
                'lilys-extra-capacity.ftl'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1349
    )
    ExtraCapacity_FR = Mod(
        id='ExtraCapacity_FR',
        modname='ExtraCapacity',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1d-GXx7NiT1KfZh57HYVRjNvT-7lNLuzH&export=download&confirm=xxx':
                'lilys-extra-capacity.ftl'
        },
        version='1.0',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=[],
        priority=1349
    )
    TemporalMasteryRU = Mod(
        id='TemporalMasteryRU',
        modname='TemporalMastery',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1xe9qBsqNFaP9Rc9ahAGlwZbEexZcR89f&export=download&confirm=xxx':
                'TemporalMastery_v0.1.7.zip'
        },
        version='0.1.7',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1350
    )
    TemporalMastery_ZH_HANS = Mod(
        id='TemporalMastery_ZH_HANS',
        modname='TemporalMastery',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1xe9qBsqNFaP9Rc9ahAGlwZbEexZcR89f&export=download&confirm=xxx':
                'TemporalMastery_v0.1.7.zip'
        },
        version='0.1.7',
        locale='zh_Hans',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['zh_Hans'],
        dependent_modnames=[],
        priority=1350
    )
    SectorMapPlusRU = Mod(
        id='SectorMapPlusRU',
        modname='SectorMapPlus',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1tpbtgM2ut8DNZ2oHO1MLXAH1kzim6eeP&export=download&confirm=xxx':
                'Beacon Map Plus.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1352
    )
    RainbowModeRU = Mod(
        id='RainbowModeRU',
        modname='RainbowMode',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1BjRP0-aG_r2fLfZvXmcR6-zUym8Px2-7&export=download&confirm=xxx':
                'FTL-Rainbow-Mode.zip'
        },
        version='1.4',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1360
    )
    TradingRU = Mod(
        id='TradingRU',
        modname='Trading',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=19B-7wTdO4XmNQQwduafLEKg4yMNk5huJ&export=download&confirm=xxx':
                'FTL-Trading-System.zip'
        },
        version='0.13',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1400
    )
    StatisticRU = Mod(
        id='StatisticRU',
        modname='Statistic',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1yCsQv0wKclOsynktBKWss-5Q6LemnV0o&export=download&confirm=xxx':
                'Statistic.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=['Brightness_Particle_System', 'Lightweight_Lua'],
        priority=1410
    )
    RandomSS_RU = Mod(
        id='RandomSS_RU',
        modname='RandomSS',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1xrGEfC-YEOH85oGQwzjhAz6NQyzOJKbC&export=download&confirm=xxx':
                'FTL-Random-Starting-Sector.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1500
    )
    MoreManSysRU = Mod(
        id='MoreManSysRU',
        modname='MoreManSys',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-3-MHlG_Xn_Pufhj9zmuxamFfbltz6f6&export=download&confirm=xxx':
                'MoreMannableSystemsV2_PATCH_LAST.zip'
        },
        version='2.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1600
    )
    MoreManSys_ZH_HANS = Mod(
        id='MoreManSys_ZH_HANS',
        modname='MoreManSys',
        download_targets={
            'https://github.com/kokoro11/more_mannable//releases/download/v2.1/MoreMannableSystemsV2_PATCH_LAST.zip':
                'MoreMannableSystemsV2_PATCH_LAST.zip'
        },
        version='2.1',
        locale='zh_Hans',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['zh_Hans'],
        dependent_modnames=[],
        priority=1600
    )
    UniversalWeaponMod_RU = Mod(
        id='UniversalWeaponMod_RU',
        modname='UniversalWeaponMod',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=11ZXbm8S_VxU2PBy4viostfpYk31Apx5q&export=download&confirm=xxx':
                'UniversalWeaponModularity.zip'
        },
        version='0.1.2',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1700
    )
    UniversalWeaponMod_ZH_HANS = Mod(
        id='UniversalWeaponMod_ZH_HANS',
        modname='UniversalWeaponMod',
        download_targets={
            'https://github.com/kokoro11/modular_weapons/releases/download/v0.2/UniversalWeaponModularity.zip':
                'UniversalWeaponModularity.zip'
        },
        version='0.2',
        locale='zh_Hans',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['zh_Hans'],
        dependent_modnames=[],
        priority=1700
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1800
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['de'],
        dependent_modnames=[],
        priority=1800
    )
    SymbiontWonderdroneRU = Mod(
        id='SymbiontWonderdroneRU',
        modname='SymbiontWonderdrone',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1SKdCZ2Z06dsfJTgjEcfr9vlohtLmNgCt&export=download&confirm=xxx':
                'SymbiontWonderdronerRUS.zip'
        },
        version='1.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1860
    )
    JudgeBlueOptionsRU = Mod(
        id='JudgeBlueOptionsRU',
        modname='JudgeBlueOptions',
        download_targets={
            'https://drive.usercontent.google.com/download?id=1-88OSmVafL30rYGhRgLB13AEL_v_xems&export=download&confirm=xxx':
                'Multiverse.-.Judge.Blue.Options.zip'
        },
        version='1.5',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=1900
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2000
    )
    BeamMasterWBH_RU = Mod(
        id='BeamMasterWBH_RU',
        modname='BeamMasterWBH',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1tQB5ZGl1UvSdfkdxvcQpja57LGP6L2Uj&export=download&confirm=xxx':
                'Beam Master will be here.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2100
    )
    HereBeMarkersRU = Mod(
        id='HereBeMarkersRU',
        modname='HereBeMarkers',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1-4sV0eYHSx1zP551s3xkB0JO5wGVCQGk&export=download&confirm=xxx':
                'Here be Markers 3.1.1.zip'
        },
        version='3.1.1',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2200
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2210
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=2300
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2300
    )
    VanUI_FR = Mod(
        id='VanUI_FR',
        modname='VanUI',
        download_targets={
            'https://drive.usercontent.google.com/u/0/uc?id=1-RSAqQI-2tBxDYy5SGtoctIis_vYD8KO&export=download&confirm=xxx':
                'Multiverse - VanUI 4.0.zip'
        },
        version='4.0',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=[],
        priority=2300
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ko'],
        dependent_modnames=[],
        priority=2300
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
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2400
    )
    HolidaySpecialRU = Mod(
        id='HolidaySpecialRU',
        modname='HolidaySpecial',
        download_targets={
            'https://drive.usercontent.google.com/u/0/uc?id=1lNkZRv92sE_AwIJXTM7X573_GtHUk1M5&export=download&confirm=xxx':
                'The Multiverse Holiday Special.zip'
        },
        version='1.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2410
    )
    NoHardModeScrap = Mod(
        id='NoHardModeScrap',
        modname='NoHardModeScrap',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1glswXprs9sRWR_9KfUPsfU6TlaqtIgtR&export=download&confirm=xxx':
                'No Hard Mode Scrap Penalty 3.0.zip'
        },
        version='3.0',
        locale='en',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=2500
    )
    NoHardModeScrapRU = Mod(
        id='NoHardModeScrapRU',
        modname='NoHardModeScrap',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1glswXprs9sRWR_9KfUPsfU6TlaqtIgtR&export=download&confirm=xxx':
                'No Hard Mode Scrap Penalty 3.0.zip'
        },
        version='3.0',
        locale='ru',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['ru'],
        dependent_modnames=[],
        priority=2500
    )
    NoHardModeScrap_FR = Mod(
        id='NoHardModeScrap_FR',
        modname='NoHardModeScrap',
        download_targets={
            'https://drive.usercontent.google.com/u/1/uc?id=1glswXprs9sRWR_9KfUPsfU6TlaqtIgtR&export=download&confirm=xxx':
                'No Hard Mode Scrap Penalty 3.0.zip'
        },
        version='3.0',
        locale='fr',
        metadata_url='https://raw.githubusercontent.com/ftl-mv-translation/mvinstaller/main/metadata_list.xml',
        compatible_mv_locale=['fr'],
        dependent_modnames=[],
        priority=2500
    )
    TOEPatchLast = Mod(
        id='TOEPatchLast',
        modname='TOEPatchLast',
        download_targets={
            'https://github.com/arcburnergit/FTL-Outer-Expansion/releases/download/v7.1.8/FTL-Outer-Expansion-PATCH_AFTER_ALL_OTHER_ADDONS.ftl':
                'FTL-Outer-Expansion-PATCH_AFTER_ALL_OTHER_ADDONS.ftl'
        },
        version='1.0.0',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=3000
    )
    
    DDPatchLast = Mod(
        id='DDPatchLast',
        modname='DDPatchLast',
        download_targets={
            'https://github.com/Naimeron/Darkest-Desire-Multiverse/releases/download/DDv4.1.4/darkestdesirevSystemPatcher_PATCH_LAST.zip':
                'darkestdesirevSystemPatcher_PATCH_LAST.zip'
        },
        version='1.0.0',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=3001
    )
    
    OGPatchLast = Mod(
        id='OGPatchLast',
        modname='OGPatchLast',
        download_targets={
            'https://github.com/arcburnergit/FTL-Old-Guard/releases/download/v2.0/FTL-Old-Guard-SYSTEM-PATCH-LAST.zip':
                'FTL-Old-Guard-SYSTEM-PATCH-LAST.zip'
        },
        version='1.0.0',
        locale='en',
        metadata_url=None,
        compatible_mv_locale=[],
        dependent_modnames=[],
        priority=3002
    )