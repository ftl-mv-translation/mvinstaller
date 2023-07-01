from pathlib import Path
import subprocess
import os
from loguru import logger
from flet import UserControl, Column, Row, icons, colors, TextButton, Stack, Image, Container, alignment
from mvinstaller.actions import downgrade_ftl, install_hyperspace, install_mods, is_java_installed
from mvinstaller.config import get_config
from mvinstaller.ftlpath import get_ftl_installation_state
from mvinstaller.ui.aboutdialog import AboutDialog
from mvinstaller.ui.busycontainer import BusyContainer
from mvinstaller.ui.configdialog import ConfigDialog
from mvinstaller.localetools import get_locale_name, localize as _
from mvinstaller.ui.errorsnackbar import ErrorSnackbar
from mvinstaller.ui.ftlpathfinderdialog import FTLPathFinderDialog
from mvinstaller.ui.infoscheme import InfoSchemeType
from mvinstaller.ui.installmodsdialog import InstallModsDialog
from mvinstaller.ui.operationcard import OperationCard
from mvinstaller.ui.progressdialog import ProgressDialog

class App(UserControl):
    def __init__(self, ftl_path=None, on_ftl_path_change=None):
        self._ftl_path = ftl_path
        self._on_ftl_path_change = on_ftl_path_change
        super().__init__()

    def open_ftl_path_finder_dialog(self):
        self._ftl_path_finder_dialog.open(self._ftl_path)

    def open_config_dialog(self):
        self._config_dialog.open()

    def open_about_dialog(self):
        self._about_dialog.open()

    def snack(self, infoscheme: InfoSchemeType, msg):
        self._error_snackbar.message(infoscheme, msg)

    @property
    def ftl_path(self):
        return self._ftl_path
    
    @ftl_path.setter
    def ftl_path(self, value):
        self._ftl_path = value
        self._update_state()
    
    def build(self):
        # Dialogs
        self._error_snackbar = ErrorSnackbar()
        self._ftl_path_finder_dialog = FTLPathFinderDialog(
            on_select=lambda newpath: (self._on_ftl_path_change(newpath) if self._on_ftl_path_change else None),
            error_snackbar=self._error_snackbar
        )
        self._progress_dialog = ProgressDialog(self._error_snackbar)
        self._config_dialog = ConfigDialog(self._error_snackbar)
        self._install_mods_dialog = InstallModsDialog(
            self._error_snackbar,
            on_install=lambda locale, addons: self._do_action(install_mods, locale, addons, self._ftl_path)
        )
        self._about_dialog = AboutDialog()

        # Cards
        self._operation_card_downgrade = OperationCard(_('operation-downgrade'))
        self._operation_card_hyperspace = OperationCard(_('operation-hyperspace'))
        self._operation_card_modding = OperationCard(_('operation-modding'))
        self._status_line = TextButton(
            text=_('status-line-multiverse'),
            icon=icons.ROCKET_LAUNCH,
            icon_color=colors.GREEN_400,
            on_click=lambda e: self._run_game()
        )
        self._busycontainer = BusyContainer(
            Column([
                Row(
                    [self._operation_card_downgrade, self._operation_card_hyperspace, self._operation_card_modding],
                    alignment='center'
                ),
                self._status_line
            ], horizontal_alignment='center', alignment='center'),
            busy=True
        )

        return [
            self._error_snackbar,
            self._ftl_path_finder_dialog,
            self._progress_dialog,
            self._config_dialog,
            self._install_mods_dialog,
            self._about_dialog,
            Column([
                Stack([
                    Container(Image('/bg.png'), alignment=alignment.center),
                    self._busycontainer
                ])
            ], alignment='center')
        ]

    def _update_state(self):
        self._busycontainer.visible = self._ftl_path is not None
        self._busycontainer.busy = True
        self.update()
        if self._ftl_path is None:
            self._ftl_path_finder_dialog.open(self._ftl_path)
        else:
            self._progress_dialog.open(self._update_operation_cards)

    def _do_action(self, func, *args, **kwargs):
        try:
            self._progress_dialog.open(func, *args, **kwargs)
        finally:
            self._update_state()

    def _update_operation_cards(self):
        logger.info('Checking installation state...')
        try:
            state = get_ftl_installation_state(self._ftl_path)
            if state is None:
                raise RuntimeError(f'Cannot fetch the installation state for {self._ftl_path}.')
        except Exception as e:
            self._busycontainer.visible = False
            self.snack(InfoSchemeType.Error, str(e))
            return

        # 0: vanilla, 1: unsure, 2: installed
        status_downgrade = 0
        status_hyperspace = 0
        status_mods = 0

        if state.ftl_executable_info is None:
            self._operation_card_downgrade.set(
                InfoSchemeType.Unknown, _('operation-downgrade-unknown'),
                None, None
            )
            status_downgrade = 1
        elif state.ftl_executable_info.downgraded:
            self._operation_card_downgrade.set(
                InfoSchemeType.Okay, _('operation-downgrade-success', {'version': state.ftl_executable_info.name}),
                None, None
            )
            status_downgrade = 2
        elif state.ftl_executable_info.downgrader is not None:
            self._operation_card_downgrade.set(
                InfoSchemeType.Warning, _('operation-downgrade-required', {'version': state.ftl_executable_info.name}),
                _('operation-downgrade-action'),
                lambda e: self._do_action(downgrade_ftl, self._ftl_path, state.ftl_executable_info.downgrader)
            )
            status_downgrade = 0
        else:
            self._operation_card_downgrade.set(
                InfoSchemeType.Error, _('operation-downgrade-unsupported', {'version': state.ftl_executable_info.name}),
                None, None
            )
            status_downgrade = 1
        
        if not state.hyperspace_installed:
            self._operation_card_hyperspace.set(
                InfoSchemeType.Warning, _('operation-hyperspace-not-installed'),
                _('operation-hyperspace-action-install'), lambda e: self._do_action(install_hyperspace, self._ftl_path)
            )
            status_hyperspace = 0
        elif state.hyperspace_info is None:
            self._operation_card_hyperspace.set(
                InfoSchemeType.Unknown, _('operation-hyperspace-unknown'),
                _('operation-hyperspace-action-update'), lambda e: self._do_action(install_hyperspace, self._ftl_path)
            )
            status_hyperspace = 1
        elif state.hyperspace_info.outdated:
            self._operation_card_hyperspace.set(
                InfoSchemeType.Warning, _('operation-hyperspace-outdated', {'version': state.hyperspace_info.name}),
                _('operation-hyperspace-action-update'), lambda e: self._do_action(install_hyperspace, self._ftl_path)
            )
            status_hyperspace = 1
        elif not state.hyperspace_info.latest:
            self._operation_card_hyperspace.set(
                InfoSchemeType.Okay, _('operation-hyperspace-success', {'version': state.hyperspace_info.name}),
                _('operation-hyperspace-action-update'), lambda e: self._do_action(install_hyperspace, self._ftl_path)
            )
            status_hyperspace = 2
        else:
            self._operation_card_hyperspace.set(
                InfoSchemeType.Okay, _('operation-hyperspace-success', {'version': state.hyperspace_info.name}),
                None, None
            )
            status_hyperspace = 2

        if state.is_ftldat_vanilla:
            self._operation_card_modding.set(
                InfoSchemeType.Warning, _('operation-modding-required'),
                _('operation-modding-action-install'), lambda e: self._install_mods_dialog.open()
            )
            status_mods = 0
        elif state.last_installed_mods is None:
            # Unknown mods are installed (possibly Multiverse)
            if state.is_ftldat_backedup:
                self._operation_card_modding.set(
                    InfoSchemeType.Warning, _('operation-modding-unknown'),
                    _('operation-modding-action-install'), lambda e: self._install_mods_dialog.open()
                )
            else:
                self._operation_card_modding.set(
                    InfoSchemeType.Warning,
                    _('operation-modding-unknown') + '\n\n' + _('operation-modding-note-noreinstall'),
                    None, None
                )
            status_mods = 1
        else:
            # Multiverse is installed with this app
            parameters = {
                'version': state.last_installed_mods.main.version,
                'locale': get_locale_name(state.last_installed_mods.main.locale),
                'commitid': (
                    f'+{state.last_installed_mods.main.commitid}'
                    if state.last_installed_mods.main.commitid else
                    ''
                )
            }
            if state.last_installed_mods.addons:
                parameters['addons_list'] = '\n'.join(
                    f' • {metadata.title} ({metadata.version})'
                    for metadata in state.last_installed_mods.addons.values()
                )
                modding_text = modding_text = _('operation-modding-success-addons', parameters)
            else:
                modding_text = _('operation-modding-success-noaddons', parameters)
            
            if state.is_ftldat_backedup:
                self._operation_card_modding.set(
                    InfoSchemeType.Okay, modding_text,
                    _('operation-modding-action-install'), lambda e: self._install_mods_dialog.open()
                )
            else:
                self._operation_card_modding.set(
                    InfoSchemeType.Okay,
                    modding_text + '\n\n' + _('operation-modding-note-noreinstall'),
                    None, None
                )
            status_mods = 2
        
        # Override the above messages (without altering status_mod) if Java is not installed
        if not is_java_installed():
            self._operation_card_modding.set(
                InfoSchemeType.Error, _('operation-modding-java-not-installed'),
                _('operation-modding-action-java'), lambda e: os.startfile('https://www.java.com/en/download/')
            )
        
        if status_downgrade == 0 and status_hyperspace == 0 and status_mods == 0:
            self._status_line.text = _('status-line-vanilla')
            self._status_line.icon_color = colors.BLUE_GREY_400
        elif status_downgrade == 2 and status_hyperspace == 2 and status_mods == 2:
            self._status_line.text = _('status-line-multiverse')
            self._status_line.icon_color = colors.GREEN_400
        else:
            self._status_line.text = _('status-line-unknown')
            self._status_line.icon_color = colors.RED_400

        get_config().last_ftl_path = str(self._ftl_path)
        get_config().save()

        self._busycontainer.busy = False
        self.update()

    def _run_game(self):
        args = [str(Path(self._ftl_path) / 'FTLGame.exe')]
        subprocess.Popen(args, cwd=str(self._ftl_path))
