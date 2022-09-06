from typing import Optional
from flet import UserControl, Dropdown, dropdown, Text, AlertDialog, TextButton, Column
from mvinstaller.config import get_config
from mvinstaller.localetools import get_locale_name
from mvinstaller.multiverse import get_mv_mainmods
from mvinstaller.localetools import localize as _
from mvinstaller.ui.busycontainer import BusyContainer
from mvinstaller.ui.errorsnackbar import ErrorSnackbar
from mvinstaller.ui.infoscheme import InfoSchemeType

class InstallModsDialog(UserControl):
    def __init__(self, error_snackbar: Optional[ErrorSnackbar]=None, on_install=None):
        self._locale_picker = None
        self._busycontainer = None
        self._dlg = None
        self._error_snackbar = error_snackbar
        self._on_install = on_install
        super().__init__()
    
    def _build_content(self):
        self._busycontainer.busy = True
        self.update()

        try:
            mainmods = get_mv_mainmods()
            if len(mainmods) == 0:
                raise RuntimeError('Failed to fetch the list of main mods')
        except Exception as e:
            if self._error_snackbar:
                self._error_snackbar.message(InfoSchemeType.Error, str(e))
            self._close(False)
            return

        mainmod_locales = [mainmod.locale for mainmod in mainmods]
        self._locale_picker.options = [dropdown.Option(locale, get_locale_name(locale)) for locale in mainmod_locales]
        if self._locale_picker.value not in mainmod_locales:
            app_locale = get_config().app_locale
            self._locale_picker.value = app_locale if app_locale in mainmod_locales else mainmod_locales[0]

        self._busycontainer.busy = False
        self.update()

    def build(self):
        self._locale_picker = Dropdown(options=[])
        self._busycontainer = BusyContainer(Column(
            [self._locale_picker],
            tight=True, horizontal_alignment='start'
        ))
        self._dlg = AlertDialog(
            modal=True,
            title=Text(_('install-mods-dialog-title')),
            content=self._busycontainer,
            actions=[
                TextButton(content=Text(_('install-mods-dialog-action-install')), on_click=lambda e: self._close(True)),
                TextButton(content=Text(_('cancel')), on_click=lambda e: self._close(False))
            ]
        )
        return self._dlg
    
    def open(self):
        self._dlg.open = True
        self._build_content()
    
    def _close(self, install):
        self._dlg.open = False
        self.update()
        if install and self._on_install:
            self._on_install(self._locale_picker.value)
