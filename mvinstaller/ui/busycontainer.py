from flet import UserControl, Column, ProgressRing

class BusyContainer(UserControl):
    def __init__(self, content=None, busy=False, *args, **kwargs):
        self._content = content
        self._busy = busy
        self._progressring = None
        self._ctrl = None
        super().__init__(*args, **kwargs)

    def build(self):
        self._progressring = ProgressRing()
        self._ctrl = Column(
            [self._content, self._progressring]
            if self._content is not None
            else [self._progressring],
            tight=True
        )
        self._progressring.visible = self._busy
        if self._content is not None:
            self._content.visible = not self._busy
        return self._ctrl

    @property
    def busy(self):
        return self._busy
    
    @busy.setter
    def busy(self, value):
        self._busy = bool(value)
        self._progressring.visible = self._busy
        if self._content is not None:
            self._content.visible = not self._busy
        self.update()

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        self._content = value
        self._ctrl.controls = [self._content, self._progressring]
    