from pathlib import Path
from glob import glob

def ensureparent(filepath):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

def glob_posix(pattern, *args, **kwargs):
    '''
    An opinionated glob.glob():
    * recursive=True by default
    * Glob only files, not directories.
    '''
    if any(kwarg not in ('pathname', 'root_dir', 'recursive') for kwarg in kwargs):
        # We don't support dir_fd
        raise RuntimeError('Unsupported kwarg passed')
    
    new_kwargs = {"recursive": True}
    new_kwargs.update(kwargs)
    
    root_dir = Path(kwargs.get('root_dir', '.'))

    results = glob(pattern, *args, **new_kwargs)
    return list(filter(
        lambda p: (root_dir / p).is_file(),
        (Path(result).as_posix() for result in results)
    ))
