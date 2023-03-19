
import re
from typing import NamedTuple


class Temperature(NamedTuple):
  hotend: float
  hotendTarget: float
  bed: float
  bedTarget: float


temperature_regex = re.compile(
    "([TB]\d*):([-+]?\d*\.?\d*)(?: ?\/)?([-+]?\d*\.?\d*)")

hardware_id_regex = re.compile('(?<=UUID:).*')


def parse_temperature(text: str) -> Temperature:
  matches = temperature_regex.findall(text)
  return Temperature(bed=float(matches[1][1]), bedTarget=float(matches[1][2]),
                     hotend=float(matches[0][1]), hotendTarget=float(matches[0][2]))


def parse_hardware_id(text: str) -> str | None:
  return hardware_id_regex.findall(text)[0]
