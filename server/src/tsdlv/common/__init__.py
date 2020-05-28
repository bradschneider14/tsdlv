import json
import pathlib
import os
import logging

logging.basicConfig(filename='tsdlv.log', level=logging.DEBUG)

_configuration = {}
_current_path = pathlib.Path(__file__).parent.absolute()

with open(os.path.join(_current_path, '..', '..', '..', 'config.json'), "r") as config_file:
  config_contents = config_file.read()
  _configuration = json.loads(config_contents)
  logging.debug(f'configuration: {_configuration}')

def get_config_value(key):
  return _configuration.get(key)