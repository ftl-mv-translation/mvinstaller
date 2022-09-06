import locale
from glob import glob
from pathlib import Path
import babel
from fluent.runtime import FluentLocalization, FluentResourceLoader
from mvinstaller.util import get_embed_dir

_APP_LOCALE_DIR = get_embed_dir() / 'locale'

def supported_app_locales():
    supported_app_locales.cached = getattr(
        supported_app_locales, 'cached', 
        [str(Path(path).parent) for path in glob('*/main.ftl', root_dir=_APP_LOCALE_DIR)]
    )
    return supported_app_locales.cached

def get_default_app_locale():
    defaultloc = locale.getdefaultlocale()[0]
    return str(babel.Locale.negotiate([defaultloc, 'en'], supported_app_locales()))

_loader = FluentResourceLoader(str(get_embed_dir() / 'locale/{locale}'))
_l10n = None
_app_locale = None

def set_locale(locale):
    global _l10n, _app_locale
    assert locale in supported_app_locales()
    _app_locale = locale
    _l10n = FluentLocalization([locale, 'en'], ['main.ftl'], _loader)

set_locale('en')

def get_locale_name(locale):
    return babel.Locale(locale).get_display_name(_app_locale)

def localize(*args, **kwargs):
    return _l10n.format_value(*args, **kwargs)
