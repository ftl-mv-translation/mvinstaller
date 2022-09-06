import functools
import subprocess
from pathlib import Path
import sys
from loguru import logger

def get_cache_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / '.cache'
    else:
        return Path(__file__).parent.parent / '.cache'

def get_embed_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent.parent

@functools.wraps(subprocess.run)
def run_checked_subprocess_with_logging_output(*args, **kwargs):
    if any(kwarg in ('stdout', 'stderr', 'check') for kwarg in kwargs):
        raise RuntimeError('Unsupported kwarg passed')

    proc = subprocess.Popen(*args, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with proc.stdout as outf:
        for line in iter(outf.readline, b''):
            logger.info(line.decode(encoding='utf-8', errors='replace').strip('\r\n'))
    exitcode = proc.wait()
    if exitcode != 0:
        raise subprocess.CalledProcessError(exitcode, kwargs.get('args', args[0]))
