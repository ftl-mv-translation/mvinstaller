from pathlib import Path
import requests
from loguru import logger
from mvinstaller.fstools import ensureparent

def download(url, dst, force):
    if Path(dst).is_file() and not force:
        logger.info(f'Using previously downloaded file from {dst}...')
        return
    try:
        tmppath = Path(f'{dst}.downloading')
        ensureparent(tmppath)

        logger.info(f'Downloading {url}...')
        chunk_count = 0
        req = requests.get(url, stream=True)
        req.raise_for_status()
        with tmppath.open('wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                f.write(chunk)

                chunk_count += 1
                if chunk_count % 10240 == 0:
                    logger.info(f'- at {chunk_count / 1024} MiB')
        
        Path(dst).unlink(missing_ok=True)
        tmppath.rename(dst)
    except:
        tmppath.unlink(missing_ok=True)
        raise
