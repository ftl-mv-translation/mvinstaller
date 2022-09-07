from flet import AppBar, Icon, TextButton, Text, IconButton, icons, colors

class MviAppBar:
    def _invoker(self, callback, *args, **kwargs):
        def eventhandler(e):
            if callback is not None:
                callback(*args, **kwargs)
        return eventhandler
    
    def __init__(self, on_ftl_path=None, on_refresh=None, on_config=None, on_about=None):
        self._appbar = AppBar(
            leading=Icon(icons.FOLDER_OPEN),
            title=TextButton(
                content=Text('Path to FTL', style='headlineSmall', overflow='ellipsis'),
                on_click=self._invoker(on_ftl_path)
            ),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                IconButton(icons.REFRESH, on_click=self._invoker(on_refresh)),
                IconButton(icons.SETTINGS, on_click=self._invoker(on_config)),
                IconButton(icons.INFO, on_click=self._invoker(on_about)),
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
    