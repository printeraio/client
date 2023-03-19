from awscrt import io
from awsiot import mqtt_connection_builder
from decouple import config

cert_path = 'src/certs/certificate.pem.crt'
key_path = 'src/certs/private.pem.key'
root_ca_path = 'src/certs/aws.pem'


def init_mqtt_connection(client_id: str):
  try:
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=config('ENDPOINT'),
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        client_bootstrap=client_bootstrap,
        ca_filepath=root_ca_path,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=6
    )
    future = mqtt_connection.connect()
    if (future.result()['session_present'] == True):
      return mqtt_connection
  except Exception as e:
    print('Connection failed with exception {}'.format(e))
