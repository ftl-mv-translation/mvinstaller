import os
from flet import AppBar, Icon, TextButton, Text, IconButton, icons, colors
from mvinstaller.localetools import localize as _

class MviAppBar:
    def _invoker(self, callback, *args, **kwargs):
        def eventhandler(e):
            if callback is not None:
                callback(*args, **kwargs)
        return eventhandler
    
    def show_app_update(self):
        self._button_update.visible = True
        self._appbar.update()
    
    def __init__(self, on_ftl_path=None, on_refresh=None, on_open_folder=None, on_config=None, on_about=None):
        self._button_update = IconButton(
            icons.UPDATE,
            on_click=lambda e: os.startfile('https://github.com/ftl-mv-translation/mvinstaller/releases/latest'),
            tooltip=_('appbar-update-tooltip'),
            visible=False,
            bgcolor=colors.GREEN_300,
            icon_color=colors.BLUE_GREY
        )
        self._appbar = AppBar(
            leading=Icon(icons.FOLDER_OPEN),
            title=TextButton(
                content=Text('Path to FTL', style='headlineSmall', overflow='ellipsis'),
                on_click=self._invoker(on_ftl_path)
            ),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                IconButton(icons.REFRESH, on_click=self._invoker(on_refresh), tooltip=_('appbar-refresh-tooltip')),
                IconButton(icons.FOLDER, on_click=self._invoker(on_open_folder), tooltip=_('appbar-open-folder-tooltip')),
                IconButton(icons.SETTINGS, on_click=self._invoker(on_config), tooltip=_('appbar-config-tooltip')),
                IconButton(icons.INFO, on_click=self._invoker(on_about), tooltip=_('appbar-about-tooltip')),
                self._button_update
            ]
        )
    
    def appbar(self):
        return self._appbar

    @property
    def ftl_path(self):
        return self._appbar.title.content.value
    
    @ftl_path.setter
    def ftl_path(self, value):
        self._appbar.title.content.value = value
    
    @property
    def ftl_path_color(self):
        return self._appbar.title.content.color
    
    @ftl_path_color.setter
    def ftl_path_color(self, value):
        self._appbar.title.content.color = value
    