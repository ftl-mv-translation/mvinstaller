import os
from flet import UserControl, Column, AlertDialog, Text, TextButton, TextField, Container
from mvinstaller.localetools import localize as _
from mvinstaller import __version__ as app_version

_ABOUT = '''Created by the FTL: Multiverse translation team.
Licensed under MIT License; see https://github.com/ftl-mv-translation/mvinstaller/blob/main/LICENSE.

FTL: Faster Than Light is a trademark of Subset Games. Unless otherwise stated, the authors and the contributors of this application is not affiliated with nor endorsed by Subset Games.
https://subsetgames.com/ftl.html

FTL: Multiverse is an overhaul mod for FTL: Faster Than Light.
https://subsetgames.com/forum/viewtopic.php?f=11&t=35332

FTL: Multiverse Translation Project is a collaborative project housed at:
https://github.com/ftl-mv-translation/ftl-mv-translation

FTL: Hyperspace is a hard-coded mod for FTL: Faster Than Light.
https://ftl-hyperspace.github.io/FTL-Hyperspace/
License notice (CC BY-SA 4.0): https://github.com/FTL-Hyperspace/FTL-Hyperspace/blob/master/LICENSE.md

Slipstream Mod Manager is a mod manager for FTL: Faster Than Light.
https://github.com/Vhati/Slipstream-Mod-Manager
License notice (GPL 2.0): https://github.com/Vhati/Slipstream-Mod-Manager/blob/master/LICENSE
'''

class AboutDialog(UserControl):
    def build(self):
        self._dlg = AlertDialog(
            modal=True,
            title=Text(_('about-dialog-title')),
            content=Column(
                [
                    Text(_('about-dialog-appname', {'version': app_version}), style='titleMedium'),
                    TextButton(
                        content=Text(_('about-dialog-repository-button')),
                        on_click=lambda e: os.startfile('https://github.com/ftl-mv-translation/mvinstaller')
                    ),
                    Container(
                        TextField(width=800, read_only=True, multiline=True, max_lines=20, text_size=12, value=_ABOUT),
                        width=800
                    )
                ],
                tight=True
            ),
            actions=[TextButton(content=Text(_('close')), on_click=lambda e: self._close())]
        )
        return self._dlg
    
    def open(self):
        self._dlg.open = True
        self.update()
    
    def _close(self):
        self._dlg.open = False
        self.update()
