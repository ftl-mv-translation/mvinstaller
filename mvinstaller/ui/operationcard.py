from flet import (
    UserControl, Icon, icons, colors, Text, ElevatedButton, Card, Container, Column, Row, Divider, alignment
)
from mvinstaller.ui.infoscheme import InfoSchemeType

class OperationCard(UserControl):
    def __init__(self, title):
        self._title = title
        super().__init__()

    def build(self):
        self._ctrl_icon = Icon(icons.WARNING_OUTLINED, color=colors.YELLOW_400, size=36)
        self._ctrl_title = Text(self._title, style='headlineSmall', weight='bold')
        self._ctrl_body = Text('abcde')
        self._ctrl_action = ElevatedButton('Do it')
        return Card(
            Container(
                Column([
                    Row(
                        [self._ctrl_icon, self._ctrl_title],
                        alignment='center'
                    ),
                    Divider(),
                    Container(self._ctrl_body, expand=True),
                    Container(self._ctrl_action, alignment=alignment.center)
                ]),
                padding=10
            ),
            width=300,
            height=300,
            margin=5
        )

    def set(self, infoscheme: InfoSchemeType, body, action_name, on_action):
        self._ctrl_icon.name = infoscheme.value.icon
        self._ctrl_icon.color = infoscheme.value.fgcolor
        self._ctrl_body.value = body
        self._ctrl_action.visible = bool(action_name)
        self._ctrl_action.text = action_name
        self._ctrl_action.on_click = on_action
        self.update()
