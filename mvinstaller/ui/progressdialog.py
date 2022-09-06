import os
import threading
from time import sleep
from typing import Optional
from loguru import logger
from flet import UserControl, TextField, AlertDialog, Text, Column, ProgressRing
from mvinstaller.ui.errorsnackbar import ErrorSnackbar
from mvinstaller.ui.infoscheme import InfoSchemeType
from mvinstaller.localetools import localize as _

class ProgressDialog(UserControl):
    def __init__(self, error_snackbar: Optional[ErrorSnackbar]=None):
        self._dlg = None
        self._logctrl = None
        self._error_snackbar = error_snackbar
        super().__init__()
    
    def build(self):
        self._logctrl = TextField(
            width=800,
            read_only=True,
            multiline=True,
            max_lines=20,
            text_size=12
        )

        self._dlg = AlertDialog(
            modal=True,
            title=Text(_('progress-dialog-title')),
            content=Column([ProgressRing(), self._logctrl], horizontal_alignment='center', width=600, tight=True),
        )
        return self._dlg

    def _logger_thread(self, rf):
        self._logctrl.value = ''
        self.update()
        for line in rf:
            self._logctrl.value += line
            self.update()
        sleep(0.5)
        self._dlg.open = False
        self.update()

    def open(self, target, *args, **kwargs):
        if self._dlg.open:
            return
        self._dlg.open = True
        r, w = os.pipe()

        with os.fdopen(r, 'r', encoding='utf-8', errors='replace', buffering=1) as rf:
            with os.fdopen(w, 'w', encoding='utf-8', buffering=1) as wf:
                sink = logger.add(wf, format='{message}', level='INFO')

                t = threading.Thread(target=self._logger_thread, args=(rf,))
                t.start()
                try:
                    target(*args, **kwargs)
                except Exception as e:
                    if self._error_snackbar:
                        self._error_snackbar.message(InfoSchemeType.Error, str(e))
                
                logger.remove(sink)
            t.join()
