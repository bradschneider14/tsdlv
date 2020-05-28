from flask.views import MethodView
from flask import request
from flask import make_response
import os
import uuid
import json
import logging

from tsdlv.common import get_config_value

class SessionsView(MethodView):
  """

  """  
  def post(self):
    logging.debug('Received POST request to session view')

    template_file = request.files.get('template_file')
    if not template_file:
      logging.debug('Error in request - no template file.')
      return make_response('Cannot create session without template', 400)
    
    # create session id and workspace
    session_id = uuid.uuid4()
    session_name = request.form.get('name', 'Unnamed Session')
    logging.debug(f'creating new session workspace for session {session_name} ({session_id})')
    
    session_data_loc = get_config_value('session_data_loc')
    session_dir_path = os.path.join(session_data_loc, str(session_id))
    os.makedirs(session_dir_path)
    logging.debug(f'workspace created! ({session_dir_path})')

    # save the uploaded template file
    template_file.save(os.path.join(session_dir_path, 'template.txt'))

    # save the metadata
    metadata = { 'id': str(session_id), 'name': session_name }

    metadata_path = os.path.join(session_dir_path, '.metadata')
    try:
      with open(metadata_path, mode="w") as metadata_file:
        metadata_file.write(json.dumps(metadata))
    except OSError as exc:
      logging.error(f'Unable to write metadata file to {metadata_path}', exc_info=exc)
      return make_response('Error creating session', 500)

    return make_response({"session_id":session_id}, 201)

  def get(self):
    sessions = []
    for root, dirs, files in os.walk(get_config_value("session_data_loc")):
      for dir_name in dirs:
        metadata_path = os.path.join(root, dir_name, '.metadata')
        try:
          with open(metadata_path, 'r') as metadata_file:
            metadata = json.loads(metadata_file.read())
            sessions.append(metadata)
        except OSError as exc:
          logging.error(f'Unable to read metadata for session {dir_name}', exc_info=exc)

    return make_response(json.dumps({"sessions":sessions}), 200)


