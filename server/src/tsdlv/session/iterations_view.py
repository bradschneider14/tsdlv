from flask.views import MethodView
from flask import request
from flask import make_response
import os
import uuid
import json
import logging

from tsdlv.common import get_config_value
from tsdlv.common.parser import Parser

class IterationsView(MethodView):
  """

  """  
  def get(self, session_id, file_id):
    logging.debug('Received GET request to iteration view')

    if (not session_id) or (not file_id):
      logging.error('Cannot get iterations without session id and file id.')
      return make_response('Cannot get iterations without a session and file.', 400)

    # build paths for the session
    session_data_loc = get_config_value('session_data_loc')
    session_dir_path = os.path.join(session_data_loc, str(session_id))
    metadata_path = os.path.join(session_dir_path, '.metadata')

    try:
      with open(metadata_path, mode="r") as metadata_file:
        metadata = json.loads(metadata_file.read())        
    except OSError as exc:
      logging.error(f'Unable to read metadata file at {metadata_path}', exc_info=exc)
      return make_response('Error reading session', 500)

    # search metadata for the specified file
    file_list = metadata.get('files', [])
    the_file_name = ''
    for f in file_list:
      if f["id"] == file_id:
        the_file_name = f["name"]
        break
    
    if not the_file_name:
      return make_response('Invalid file id.', 500)
    
    # load the template
    template_path = os.path.join(session_dir_path, 'template.txt')
    try:
      with open(template_path, mode="r") as template_file:
        template = json.loads(template_file.read())        
    except OSError as exc:
      logging.error(f'Unable to read template file at {template_path}', exc_info=exc)
      return make_response('Error reading session', 500)

    # parse the file
    the_file_path = os.path.join(session_dir_path, the_file_name)
    try:
      with open(the_file_path, "r") as the_file:
        parser = Parser(template)
        iterations = parser.get_iterations(the_file.read())
    except OSError as exc:
      logging.error(f'Unable to read file at {template_path}', exc_info=exc)
      return make_response('Error reading file', 500)

    return make_response({'iterations':iterations}, 200)

