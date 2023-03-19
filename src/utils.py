
import datetime
import re
from typing import NamedTuple


class Temperature(NamedTuple):
  hotend: float
  hotendTarget: float
  bed: float
  bedTarget: float
  createdAt: str


temperature_regex = re.compile(
    "([TB]\d*):([-+]?\d*\.?\d*)(?: ?\/)?([-+]?\d*\.?\d*)")

hardware_id_regex = re.compile('(?<=UUID:).*')


def parse_temperature(text: str) -> Temperature:
  createdAt = datetime.datetime.utcnow().replace(
      tzinfo=datetime.timezone.utc).isoformat()
  matches = temperature_regex.findall(text)
  return Temperature(bed=float(matches[1][1]), bedTarget=float(matches[1][2]),
                     hotend=float(matches[0][1]), hotendTarget=float(matches[0][2]), createdAt=createdAt)


def parse_hardware_id(text: str) -> str | None:
  return hardware_id_regex.findall(text)[0]
