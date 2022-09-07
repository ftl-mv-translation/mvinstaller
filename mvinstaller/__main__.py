from pathlib import Path
from flet import Page, colors, app as flet_app, theme
from mvinstaller.config import get_config
from mvinstaller.localetools import localize as _, set_locale
from mvinstaller.ui.app import App
from mvinstaller.ui.appbar import MviAppBar
from mvinstaller.util import get_embed_dir

def index(page: Page):
    page.title = _('app-title')
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.theme_mode = 'dark'
    page.dark_theme = theme.Theme(color_scheme_seed=colors.BLUE_GREY, visual_density='comfortable')
    page.bgcolor = colors.BLACK
    page.update()

    def on_ftl_path_change(ftl_path):
        if ftl_path:
            appbar.ftl_path = ftl_path
            appbar.ftl_path_color = colors.WHITE
        else:
            appbar.ftl_path = _('topbar-ftl-not-found-warning')
            appbar.ftl_path_color = colors.RED_100
        page.update()

        app.ftl_path = ftl_path

    app = App(on_ftl_path_change=on_ftl_path_change)
    appbar = MviAppBar(
        on_refresh=lambda: on_ftl_path_change(app.ftl_path),
        on_ftl_path=app.open_ftl_path_finder_dialog,
        on_config=app.open_config_dialog,
        on_about=app.open_about_dialog
    )
    page.appbar = appbar.appbar()
    page.add(app)
    on_ftl_path_change(None if get_config().last_ftl_path is None else Path(get_config().last_ftl_path))

def main():
    set_locale(get_config().app_locale)
    flet_app(target=index, assets_dir=str(get_embed_dir() / 'assets'))

if __name__ == '__main__':
    main()
