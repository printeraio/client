import time
from queue import Queue
from typing import NamedTuple

import simplejson as json
from decouple import config
from printrun.printcore import printcore

from constants import COMMANDS
from printer.mqtt_connection import QoS, init_mqtt_connection
from utils import Temperature, parse_temperature

PRINTER_ID = config('PRINTER_ID')
CLIENT_ID = config('CLIENT_ID')
HARDWARE_ID = config('HARDWARE_ID')


class Telemetry(NamedTuple):
  temperature: Temperature
  printerId: str
  hardwareId: str


def receive_callback(line: str, queue: Queue):
  if ('T:' in line and 'B:' in line):
    temperature = parse_temperature(line)
    telemetry = Telemetry(temperature=temperature,
                          printerId=PRINTER_ID, hardwareId=HARDWARE_ID)
    queue.put(telemetry)


def init_printer(port: str, baud_rate: str):
  printer = printcore(port, baud_rate)
  telemetry_queue = Queue()
  while not printer.online:
    time.sleep(0.1)

  printer.recvcb = lambda e: receive_callback(e, telemetry_queue)
  mqtt_connection = init_mqtt_connection(CLIENT_ID)

  while True:
    printer.send_now(command=COMMANDS.REPORT_TEMPERATURES.value)
    if not telemetry_queue.empty():
      telemetry = telemetry_queue.get()
      print(f"{CLIENT_ID}/{PRINTER_ID}", telemetry)
      mqtt_connection.publish(topic=f"{CLIENT_ID}/{PRINTER_ID}", payload=json.dumps(telemetry, namedtuple_as_object=True),
                              qos=QoS.AT_LEAST_ONCE)
    time.sleep(1)
    # printer <-
