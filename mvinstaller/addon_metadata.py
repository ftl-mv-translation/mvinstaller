from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from lxml import etree
from loguru import logger
from mvinstaller.signatures import FixedAddonsList
from mvinstaller.util import get_embed_dir

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

def _init_metadata():
    ret = {}
    for addon in FixedAddonsList:
        try:
            metadata = read_metadata(get_embed_dir() / 'addon_metadata' / f'{addon.name}.xml')
            ret[addon.name] = metadata
        except Exception as e:
            logger.error(f'Error while reading metadata for {addon.name}: {e}. Skipping...')
    return ret

_CACHED_METADATA = None

def init_metadata():
    global _CACHED_METADATA
    if _CACHED_METADATA is None:
        _CACHED_METADATA = _init_metadata()

def get_metadata(metadata_name):
    init_metadata()
    return _CACHED_METADATA.get(metadata_name, Metadata(metadata_name, None, 'Unknown', None, ''))

def metadata_text(metadata):
    ret = metadata.title
    if metadata.version:
        ret += f' (version {metadata.version})'
    ret += f'\nBy {metadata.author}'
    if metadata.url:
        ret += f'\n{metadata.url}'
    ret += f'\n\n{metadata.description}'
    return ret
