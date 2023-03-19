from enum import Enum

IS_DEV = True


class COMMANDS(Enum):
  REPORT_TEMPERATURES = 'M105\n'
