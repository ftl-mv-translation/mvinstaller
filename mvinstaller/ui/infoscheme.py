from collections import namedtuple
from enum import Enum
from flet import colors, icons

InfoScheme = namedtuple('InfoScheme', ('icon', 'fgcolor', 'bgcolor'))

class InfoSchemeType(Enum):
    Error = InfoScheme(icons.CLOSE, colors.RED_400, colors.RED_100)
    Okay = InfoScheme(icons.CHECK, colors.GREEN_400, colors.GREEN_100)
    Warning = InfoScheme(icons.WARNING, colors.YELLOW_400, colors.YELLOW_100)
    Unknown = InfoScheme(icons.QUESTION_MARK, colors.YELLOW_400, colors.YELLOW_100)

