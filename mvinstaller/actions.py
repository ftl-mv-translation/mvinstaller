import zipfile
import subprocess
import shutil
from pathlib import Path
import javaproperties
from loguru import logger
from mvinstaller.fstools import glob_posix
from mvinstaller.multiverse import clear_expired_mainmods, get_mv_mainmods
from mvinstaller.webtools import download
from mvinstaller.util import get_cache_dir, run_checked_subprocess_with_logging_output
from mvinstaller.ftlpath import get_ftl_installation_state, get_latest_hyperspace
from mvinstaller.localetools import get_locale_name

def _extract_without_path(zipf, name, dstdir):
    # Trick from https://stackoverflow.com/a/47632134/3567518
    info = zipf.getinfo(name)
    info.filename = Path(info.filename).name
    zipf.extract(info, dstdir)

def downgrade_ftl(ftl_path, downgrader):
    if downgrader == 'steam':
        ftl_path = Path(ftl_path)
        cache_dir = get_cache_dir()
        latest_hyperspace = get_latest_hyperspace()

        download(latest_hyperspace.url, cache_dir / latest_hyperspace.filename, False)

        logger.info('Extracting archive...')
        with zipfile.ZipFile(cache_dir / latest_hyperspace.filename) as zipf:
            _extract_without_path(
                zipf, 'Windows - Extract these files into where FTLGame.exe is/patch/flips.exe', cache_dir
            )
            _extract_without_path(
                zipf, 'Windows - Extract these files into where FTLGame.exe is/patch/patch.bps', cache_dir
            )
        
        logger.info('Backing up original EXE in FTLGame_orig.exe...')
        shutil.copyfile(ftl_path / 'FTLGame.exe', ftl_path / 'FTLGame_orig.exe')

        logger.info('Patching...')
        run_checked_subprocess_with_logging_output(
            [str(cache_dir / 'flips.exe'), '-a', str(cache_dir / 'patch.bps'), str(ftl_path / 'FTLGame.exe')]
        )
    else:
        assert False

def install_hyperspace(ftl_path):
    ftl_path = Path(ftl_path)
    cache_dir = get_cache_dir()
    latest_hyperspace = get_latest_hyperspace()

    download(latest_hyperspace.url, cache_dir / latest_hyperspace.filename, False)

    logger.info('Extracting archive...')
    with zipfile.ZipFile(cache_dir / latest_hyperspace.filename) as zipf:
        FILES = ['Hyperspace.dll', 'lua-5.3.dll', 'xinput1_4.dll']
        for fn in FILES:
            _extract_without_path(zipf, f'Windows - Extract these files into where FTLGame.exe is/{fn}', ftl_path)

def install_mods(locale_mv, ftl_path):
    ftl_path = Path(ftl_path)

    # Find vanilla dat
    logger.info('Finding vanilla dat file...')
    installation_state = get_ftl_installation_state(ftl_path)
    if not (installation_state.is_ftldat_vanilla or installation_state.is_ftldat_backedup):
        raise RuntimeError('Cannot find vanilla dat file.')
    use_backup = installation_state.is_ftldat_backedup

    cache_dir = get_cache_dir()

    def check_java():
        logger.info('Checking if Java is available...')
        try:
            subprocess.run(['java', '-version'], check=True)
        except:
            raise RuntimeError(
                'Java does not seem to be installed. JRE is required for running Slipstream Mod Manager.'
            )
    
    def install_slipstream():
        # Note: A proper distribution comes from Sourceforge (https://sourceforge.net/projects/slipstreammodmanager/).
        #       Windows distribution for 1.9.1 has been copied the to the ftlmv-weblate-bot GDrive,
        #       as it's a bit tricky to implement a programmatic downloader for SF.
        download(
            'https://drive.google.com/uc?id=194uP5DHmI7bU56soStbv4MfRat2xpXiu&confirm=t',
            cache_dir / 'SlipstreamModManager_1.9.1-Win.zip',
            False
        )

        logger.info('Extracting archive...')
        with zipfile.ZipFile(cache_dir / 'SlipstreamModManager_1.9.1-Win.zip') as zipf:
            zipf.extractall(cache_dir)
        smmbase = cache_dir / 'SlipstreamModManager_1.9.1-Win'
        
        logger.info('Writing SMM config...')
        with (smmbase / 'modman.cfg').open('w') as f:
            javaproperties.dump({'ftl_dats_path': str(ftl_path)}, f)
        
        logger.info('Copying vanilla dat file to SMM...')
        shutil.copy(ftl_path / ('ftl.dat.vanilla' if use_backup else 'ftl.dat'), smmbase / 'backup/ftl.dat.bak')

        return smmbase
    
    def install_multiverse(smmbase):
        clear_expired_mainmods(glob_posix(str(smmbase / 'mods/*')))

        mainmods = get_mv_mainmods()
        mainmod = next(mainmod for mainmod in mainmods if mainmod.locale == locale_mv)

        logger.info(
            f'[Target main mod] FTL: Multiverse {mainmod.version}, {get_locale_name(mainmod.locale)}'
            + (f' at commitid {mainmod.commitid}' if mainmod.commitid else '')
        )
        for url, fn in mainmod.download_targets.items():
            download(url, smmbase / 'mods' / fn, False)

        if not use_backup:
            logger.info('Creating backup for dat...')
            shutil.copy(ftl_path / 'ftl.dat', ftl_path / 'ftl.dat.vanilla')
        
        logger.info('Running patch...')
        run_checked_subprocess_with_logging_output(
            [smmbase / 'modman.exe', '--patch', *mainmod.download_targets.values()]
        )

    check_java()
    smmbase = install_slipstream()
    install_multiverse(smmbase)
