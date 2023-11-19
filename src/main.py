import threading

from constants import IS_DEV
from ports import DEFAULT_PORTS, check_printer
from printer import init_printer
from printer.mqtt_connection import init_mqtt_connection

if __name__ == '__main__':
  printers = DEFAULT_PORTS if (IS_DEV) else check_printer()
  for printer in printers:
    port, baud_rate, _ = printer
    printer_thread = init_printer(
        port=port, baud_rate=baud_rate)
    worker = threading.Thread(target=printer_thread)
    worker.start()
