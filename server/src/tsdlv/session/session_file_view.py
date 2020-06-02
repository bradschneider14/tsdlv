from flask.views import MethodView
from flask import request
from flask import make_response
import os
import uuid
import json
import logging

from tsdlv.common import get_config_value

class SessionFileView(MethodView):
  """

  """  
  def post(self, session_id):
    logging.debug('Received POST request to session file view')

    if not session_id:
      logging.error('Cannot upload a file without a session id.')
      return make_response('Cannot upload a file without a session.', 400)

    new_file = request.files.get('new_file')
    if not new_file:
      logging.debug('Error in request - no file uploaded.')
      return make_response('No file uploaded.', 400)
    
    session_data_loc = get_config_value('session_data_loc')
    session_dir_path = os.path.join(session_data_loc, str(session_id))
    if not os.path.exists(session_dir_path):
      logging.error(f'No session workspace found for session id {session_id}')
      return make_response('Invalid session', 400)

    # save the uploaded file
    new_file.save(os.path.join(session_dir_path, new_file.filename))

    # update the metadata
    metadata_path = os.path.join(session_dir_path, '.metadata')
    metadata = None
    try:
      with open(metadata_path, mode="r") as metadata_file:
        metadata = json.loads(metadata_file.read())
        logging.debug(f'Original metadata: {metadata}')
      
      if not metadata:
        logging.error(f'Unable to read metadata from file {metadata_path}')
        return make_response('Error updating session', 500)

      if not 'files' in metadata:
        metadata['files'] = []
      metadata['files'].append({'id': str(uuid.uuid4()), 'name': new_file.filename})        
      
      with open(metadata_path, mode="w") as metadata_file:
        metadata_file.write(json.dumps(metadata))

    except OSError as exc:
      logging.error(f'Unable to update metadata file at {metadata_path}', exc_info=exc)
      return make_response('Error updating session', 500)

    return make_response("success", 201)

  def get(self, session_id):
    logging.debug('Received GET request to session file view')

    if not session_id:
      logging.error('Cannot get files without a session id.')
      return make_response('Cannot get files without a session.', 400)

    session_data_loc = get_config_value('session_data_loc')
    session_dir_path = os.path.join(session_data_loc, str(session_id))
    metadata_path = os.path.join(session_dir_path, '.metadata')
    try:
      with open(metadata_path, mode="r") as metadata_file:
        metadata = json.loads(metadata_file.read())
        file_response = {'files': metadata.get('files', [])}
        return make_response(json.dumps(file_response), 200)
        
    except OSError as exc:
      logging.error(f'Unable to update metadata file at {metadata_path}', exc_info=exc)
      return make_response('Error updating session', 500)


