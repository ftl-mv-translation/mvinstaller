from pathlib import Path
from flet import (
    Page, Text, AppBar, Icon, icons, colors, IconButton, TextButton, Container, padding, app as flet_app, theme
)
from mvinstaller.config import get_config
from mvinstaller.localetools import localize as _, set_locale
from mvinstaller.ui.app import App
from mvinstaller.util import get_embed_dir

def index(page: Page):
    page.title = _('app-title')
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.theme_mode = 'dark'
    page.dark_theme = theme.Theme(color_scheme_seed=colors.BLUE_GREY)
    page.bgcolor = colors.BLACK
    page.update()

    def on_ftl_path_change(ftl_path):
        if ftl_path:
            page.appbar.title.content.value = ftl_path
            page.appbar.title.content.color = colors.WHITE
        else:
            page.appbar.title.content.value = _('topbar-ftl-not-found-warning')
            page.appbar.title.content.color = colors.RED_100
        page.update()

        app.ftl_path = ftl_path

    app = App(on_ftl_path_change=on_ftl_path_change)
    hpadded = lambda ctrl: Container(ctrl, padding=padding.Padding(15, 0, 15, 0))
    page.appbar = AppBar(
        leading=hpadded(Icon(icons.FOLDER_OPEN)),
        title=TextButton(
            content=Text('Path to FTL', style='headlineMedium', overflow='ellipsis'),
            on_click=lambda e: app.open_ftl_path_finder_dialog()
        ),
        center_title=False,
        bgcolor=colors.SURFACE_VARIANT,
        actions=[
            hpadded(IconButton(icons.SETTINGS, on_click=lambda e: app.open_config_dialog())),
        ],
    )
    page.add(app)
    on_ftl_path_change(None if get_config().last_ftl_path is None else Path(get_config().last_ftl_path))

def main():
    set_locale(get_config().app_locale)
    flet_app(target=index, assets_dir=str(get_embed_dir() / 'assets'))

if __name__ == '__main__':
    main()
