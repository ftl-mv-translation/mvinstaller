import shutil
from pathlib import Path
from zipfile import ZipFile
from mvinstaller.fstools import extract_without_path
from mvinstaller.signatures import AddonsList
from mvinstaller.webtools import download
from loguru import logger

def check_and_overwrite(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not dst.is_file():
        logger.info('-> new addon')
        shutil.move(src, dst)
    else:
        with open(src, 'rb') as srcf:
            with open(dst, 'rb') as dstf:
                if srcf.read() == dstf.read():
                    logger.info('-> no change on metadata.xml')
                    return
    
        logger.info('-> updating to a new metadata.xml')
        shutil.move(src, dst)

def fetch_metadata(addon):
    # Use the first URL
    url, fn = next(iter(addon.download_targets.items()))

    build_dir = Path('build')
    download(url, build_dir / fn, True)
    with ZipFile(build_dir / fn) as zipf:
        extract_without_path(zipf, 'mod-appendix/metadata.xml', build_dir)
        
    check_and_overwrite(build_dir / 'metadata.xml', f'addon_metadata/{addon.metadata_name}.xml')
    
def main():
    for addon in AddonsList:
        addon = addon.value
        if addon.custom_metadata:
            logger.info(f'[{addon.metadata_name}] Skipped, using custom metadata...')
            continue
        logger.info(f'[{addon.metadata_name}] Fetching...')
        fetch_metadata(addon)

main()