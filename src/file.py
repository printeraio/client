import os
import urllib.request


def download_gcode_file(url, filename):
  is_exists = os.path.exists(f'{os.getcwd()}/files')
  if not is_exists:
    os.makedirs(f'{os.getcwd()}/files')

  response = urllib.request.urlretrieve(url, f'{os.getcwd()}/files/{filename}')
  return True if response[0] else False
