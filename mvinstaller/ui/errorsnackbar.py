from flet import UserControl, icons, Icon, Text, SnackBar, Row
from mvinstaller.ui.infoscheme import InfoSchemeType

class ErrorSnackbar(UserControl):
    def __init__(self):
        self._ctrl_icon = None
        self._ctrl_text = None
        self._ctrl_snackbar = None
        super().__init__()

    def build(self):
        self._ctrl_icon = Icon(name=icons.CHECK)
        self._ctrl_text = Text('text')
        self._ctrl_snackbar = SnackBar(content=Row([self._ctrl_icon, self._ctrl_text]))
        return self._ctrl_snackbar
    
    def message(self, infoscheme: InfoSchemeType, msg):
        self._ctrl_icon.name = infoscheme.value.icon
        self._ctrl_icon.color = infoscheme.value.fgcolor
        self._ctrl_text.value = msg
        self._ctrl_snackbar.bgcolor = infoscheme.value.bgcolor
        self._ctrl_snackbar.open = True
        self.update()
