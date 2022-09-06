from pathlib import Path
from typing import Optional
from flet import UserControl, FilePicker, AlertDialog, Text, Stack, ElevatedButton, Column, icons, colors
from mvinstaller.ftlpath import get_ftl_installation_state, get_ftl_path_candidates
from mvinstaller.ui.busycontainer import BusyContainer
from mvinstaller.ui.errorsnackbar import ErrorSnackbar
from mvinstaller.ui.infoscheme import InfoSchemeType
from mvinstaller.localetools import localize as _

class FTLPathFinderDialog(UserControl):
    def __init__(self, on_select=None, error_snackbar: Optional[ErrorSnackbar]=None):
        self._dlg = None
        self._busycontainer = None
        self._filepicker = None
        self._on_select = on_select
        self._error_snackbar = error_snackbar
        super().__init__()

    def _on_choose_path(self, path):
        self._busycontainer.busy = True
        self.update()
        try:
            if path is None:
                return
            path = Path(path)
            try:
                state = get_ftl_installation_state(path)
                if state is None:
                    raise RuntimeError(f'{path} does not seem to be a valid FTL installation path.')
            except Exception as e:
                if self._error_snackbar:
                    self._error_snackbar.message(InfoSchemeType.Error, str(e))
                return
            self._dlg.open = False
            self.update()
            self._on_select(path)
        finally:
            self._busycontainer.busy = False
            self.update()

    def _build_content(self, current_path):
        def onclick_callback_func_for(path):
            def onclick(e):
                self._dlg.open = False
                self.update()
                self._on_select(path)
            return onclick

        self._busycontainer.busy = True
        self.update()

        ftl_path_candidates = get_ftl_path_candidates(additional_paths=[current_path] if current_path else None)
        
        contentcolumn = self._busycontainer.content
        contentcolumn.clean()
        for path, state in ftl_path_candidates.items():
            if isinstance(state, Exception):
                disabled = True
                infoscheme = InfoSchemeType.Error
                name = f'{_("error-indicator")} | {path}'
                icon = icons.CLOSE
                tooltip = str(state)
            else:
                disabled = False
                icon = icons.RADIO_BUTTON_CHECKED if path == current_path else icons.RADIO_BUTTON_UNCHECKED
                tooltip = None
                if state is None:
                    infoscheme = InfoSchemeType.Unknown
                    name = f'{_("unknown-version")} | {path}'
                else:
                    infoscheme = InfoSchemeType.Okay
                    name = f'{state.ftl_executable_info.name} | {path}'

            contentcolumn.controls.append(ElevatedButton(
                name,
                disabled=disabled,
                icon=icon,
                icon_color=infoscheme.value.fgcolor,
                tooltip=tooltip,
                on_click=onclick_callback_func_for(path)
            ))

        contentcolumn.controls.append(
            ElevatedButton(
                _('choose-path-button'),
                icon=icons.FOLDER_OPEN,
                icon_color=colors.YELLOW_400,
                on_click=lambda e: self._filepicker.get_directory_path(dialog_title=_('choose-path-dialog-title'))
            )
        )
        self._busycontainer.busy = False
        self.update()
    
    def build(self):
        self._filepicker = FilePicker(on_result=lambda e: self._on_choose_path(e.path))
        self._busycontainer = BusyContainer(Column(tight=True, alignment='start', horizontal_alignment='start'))
        self._dlg = AlertDialog(
            modal=True,
            title=Text(_('ftl-installation-path-dialog-title')),
            content=Stack([self._filepicker, self._busycontainer]),
            actions_alignment='end',
        )
        return self._dlg
    
    def open(self, current_path):
        self._dlg.open = True
        self._build_content(current_path)