import subprocess
import sys
from mvinstaller import __version__ as old_version
from loguru import logger

def main(new_version):
    if old_version == new_version:
        logger.info(f'already at {new_version}')
        return

    with open('mvinstaller/__init__.py', 'w') as f:
        f.write(f"__version__ = '{new_version}'\n")
    subprocess.run(['poetry', 'version', new_version], check=True)

    subprocess.run(['git', 'commit', '-a', '-m', f'Bump version to {new_version}'], check=True)
    subprocess.run(['git', 'push', 'origin'], check=True)
    subprocess.run(['git', 'tag', f'v{new_version}'], check=True)
    subprocess.run(['git', 'push', 'origin', f'v{new_version}'], check=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(input(f'enter new version(current version is {old_version})>>>'))
