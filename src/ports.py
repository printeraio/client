
import glob
import time
from typing import NamedTuple

from decouple import config
from printrun.printcore import printcore

from utils import parse_hardware_id


class Port(NamedTuple):
  port: str
  baud_rate: int
  hardware_id: str


BAUD_RATES = [2400, 9600, 19200, 38400, 57600, 115200, 250000, 500000, 1000000]
PRINTER_CONNECTION_TIMEOUT = 2
DEFAULT_PORTS = [Port(port='/dev/tty.usbserial-140', baud_rate=250000,
                      hardware_id=config('HARDWARE_ID'))]


def list_ports() -> list[str]:
  ports: list[str] = []
  for g in ['/dev/ttyUSB*', '/dev/ttyACM*', "/dev/tty.*", "/dev/cu.*", "/dev/rfcomm*"]:
    ports += glob.glob(g)
  return ports


def errorcb(line, errors, p):
  if (len(line)):
    errors.append(line)
    p.disconnect()


def recv(line, received, hardware_id):
  if (len(line)):
    received.append(line)
    if line.startswith('FIRMWARE_NAME'):
      uuid = parse_hardware_id(line)
      print(f"Printer UUID: {uuid}")
      if (uuid):
        hardware_id.append(uuid)


def check_printer() -> list[Port]:
  printers = []
  ports = list_ports()
  for port in ports:
    if (port.lower().count('bluetooth') > 0 or port.lower().count('wlan') > 0):
      continue
    for baud_rate in BAUD_RATES:
      errors = []
      received = []
      hardware_id = []
      print('Checking port:', port, 'with baud rate:', baud_rate)
      p = printcore(port, baud_rate)

      if (p.printer == None):
        continue

      p.recvcb = lambda e: recv(e, received, hardware_id)
      p.errorcb = lambda e: errorcb(e, errors, p)

      i = 0
      while not p.online and len(errors) == 0:
        time.sleep(0.1)
        i += 0.1
        if (i > PRINTER_CONNECTION_TIMEOUT):
          break

      if (p.online):
        p.send_now('M115')
        while (len(hardware_id) == 0):
          time.sleep(0.1)
        p.disconnect()
        printer_exists = False
        for printer in printers:
          if (hardware_id[0] == printer['hardware_id']):
            printer_exists = True
        if (not printer_exists):

          printers.append(Port(port=port, baud_rate=baud_rate,
                          hardware_id=hardware_id[0]))
      else:
        p.disconnect()

  return printers
