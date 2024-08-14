from pathlib import Path
import requests
from loguru import logger
from mvinstaller.fstools import ensureparent

def _check_response_content_length(resp):
    # SEE: https://blog.petrzemek.net/2018/04/22/on-incomplete-http-reads-and-the-requests-library-in-python/
    # Code copied from the referenced blog post.
    # TL;DR: requests 2.x does NOT check premature connection closes.
    
    expected_length = resp.headers.get('Content-Length')
    if expected_length is not None:
        actual_length = resp.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError(
                'incomplete read ({} bytes read, {} more expected)'.format(
                    actual_length,
                    expected_length - actual_length
                )
            )

def download(url, dst, force, headers=None):
    if Path(dst).is_file() and not force:
        logger.info(f'Using previously downloaded file from {dst}...')
        return
    try:
        tmppath = Path(f'{dst}.downloading')
        ensureparent(tmppath)

        logger.info(f'Downloading {url}...')
        chunk_count = 0
        resp = requests.get(url, stream=True, headers=headers)
        resp.raise_for_status()
        with tmppath.open('wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                f.write(chunk)

                chunk_count += 1
                if chunk_count % 10240 == 0:
                    logger.info(f'- at {chunk_count / 1024} MiB')
        
        _check_response_content_length(resp)

        Path(dst).unlink(missing_ok=True)
        tmppath.rename(dst)
    except:
        tmppath.unlink(missing_ok=True)
        raise
