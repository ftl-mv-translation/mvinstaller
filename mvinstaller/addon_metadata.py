from time import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from lxml import etree
from loguru import logger
from mvinstaller.multiverse import get_addons, get_mv_mainmods
from mvinstaller.signatures import Mod
from mvinstaller.util import get_cache_dir, sha256
from mvinstaller.webtools import download
from mvinstaller.localetools import localize as _

@dataclass(frozen=True)
class Metadata:
    title: str
    url: Optional[str]
    author: str
    version: Optional[str]
    description: str

def read_metadata(path, metadata_name=None):
    path = Path(path)
    metadata_name = metadata_name or path.stem

    tree = etree.parse(path)

    def read(xpath, default):
        q = tree.xpath(xpath)
        return q[0].text.strip() if len(q) > 0 else default
    
    return Metadata(
        title=read('/metadata/title', metadata_name),
        url=read('/metadata/threadUrl', None),
        author=read('/metadata/author', 'Unknown'),
        version=read('/metadata/version', None),
        description=read('/metadata/description', ''),
    )

_cached_metadata = dict()

def init_metadata(mods: list[Mod]):
    global _cached_metadata

    for mod in mods:
        if mod.metadata_url is None:
            continue
        
        try:
            fn = get_cache_dir() / 'metadata' / f'{sha256(mod.id)}.xml'
            if not fn.exists() or (fn.stat().st_mtime + 3600 < time()):
                logger.info(f'Downloading metadata for {mod.id}...')
                download(mod.metadata_url, fn, True)
            metadata = read_metadata(fn)
            _cached_metadata[mod.id] = metadata
        except Exception as e:
            logger.error(f'Error while reading metadata for {mod.id}: {e}. Skipping...')


def get_metadata(id: str):
    return _cached_metadata.get(id, Metadata(id, None, 'Unknown', None, _('progress-dialog-title')))

def metadata_text(metadata):
    ret = metadata.title
    if metadata.version:
        ret += f' (version {metadata.version})'
    ret += f'\nBy {metadata.author}'
    if metadata.url:
        ret += f'\n{metadata.url}'
    ret += f'\n\n{metadata.description}'
    return ret
