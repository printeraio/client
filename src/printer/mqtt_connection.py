import time
from enum import IntEnum

from decouple import config
from paho.mqtt import client as mqtt

ca_certs = 'src/certs/ca.pem'
certfile = 'src/certs/client.pem'
keyfile = 'src/certs/client.key'


class QoS (IntEnum):
  AT_MOST_ONCE = 0
  AT_LEAST_ONCE = 1
  EXACTLY_ONCE = 2


def init_mqtt_connection(client_id: str):
  client = mqtt.Client(client_id=client_id)
  try:
    client.enable_logger()
    client.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile,
                   tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(False)
    client.connect(config('MQTT_HOST'), int(config('MQTT_PORT')), 60)
    return client

  except Exception as e:

    print('Connection failed with exception {}'.format(e))
