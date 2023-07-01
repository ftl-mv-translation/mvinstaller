import os
from flet import UserControl, dropdown, Column, Checkbox, AlertDialog, Text, TextButton, Dropdown
from mvinstaller.config import get_config
from mvinstaller.localetools import get_locale_name, supported_app_locales, localize as _

class ConfigDialog(UserControl):
    def __init__(self, error_snackbar=None):
        self._error_snackbar = error_snackbar
        self._config = get_config()
        super().__init__()

    def _on_locale_change(self, e):
        if not self._dlg.open:
            return
        self._config.app_locale = e.control.value
        self._config.save()
    
    def build(self):
        self._locale_picker = Dropdown(
            options=[dropdown.Option(locale, get_locale_name(locale)) for locale in supported_app_locales()],
            on_change=self._on_locale_change
        )
        self._dlg = AlertDialog(
            modal=True,
            title=Text(_('config-dialog-title')),
            content=Column(
                [
                    Text(_('config-language-label')),
                    self._locale_picker
                ],
                tight=True
            ),
            actions=[TextButton(content=Text(_('close')), on_click=lambda e: self._close())]
        )
        return self._dlg
    
    def open(self):
        self._locale_picker.value = self._config.app_locale
        self._dlg.open = True
        self.update()
    
    def _close(self):
        self._dlg.open = False
        self.update()
