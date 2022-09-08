from dataclasses import dataclass
from typing import Optional
from lxml import etree
from loguru import logger
from mvinstaller.signatures import AddonsList
from mvinstaller.util import get_embed_dir

@dataclass
class Metadata:
    title: str
    url: Optional[str]
    author: str
    version: Optional[str]
    description: str

def _read_metadata(metadata_name):
    tree = etree.parse(get_embed_dir() / 'addon_metadata' / f'{metadata_name}.xml')

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
    for addon in AddonsList:
        try:
            metadata = _read_metadata(addon.value.metadata_name)
            ret[addon.value.metadata_name] = metadata
        except Exception as e:
            logger.error(f'Error while reading metadata for {addon.value.metadata_name}: {e}. Skipping...')
    return ret

def get_metadata():
    cached = getattr(get_metadata, 'cached', None)
    if cached is None:
        cached = get_metadata.cached = _init_metadata()
    return cached

def metadata_text(metadata):
    ret = metadata.title
    if metadata.version:
        ret += f' (version {metadata.version})'
    ret += f'\nBy {metadata.author}'
    if metadata.url:
        ret += f'\n{metadata.url}'
    ret += f'\n\n{metadata.description}'
    return ret