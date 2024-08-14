from dataclasses import dataclass, asdict
import json
import dacite
from mvinstaller.localetools import get_default_app_locale
from mvinstaller.util import get_cache_dir
from mvinstaller.fstools import ensureparent

_CONFIG_PATH = get_cache_dir() / 'config.json'
_CONFIG = None

@dataclass
class Config:
    app_locale: str
    last_ftl_path: str

    @staticmethod
    def load(path=_CONFIG_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            return dacite.from_dict(Config, json.load(f))
    
    def save(self, path=_CONFIG_PATH):
        ensureparent(path)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f)

    @staticmethod
    def get_default():
        return Config(get_default_app_locale(), None)

def get_config():
    global _CONFIG

    if _CONFIG is None:
        try:
            _CONFIG = Config.load()
        except Exception:
            print('Cannot read config; using default config instead.')
            _CONFIG = Config.get_default()
            _CONFIG.save()

    return _CONFIG
