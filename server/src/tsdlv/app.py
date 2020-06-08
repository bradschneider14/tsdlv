from flask import Flask
from flask_cors import CORS
from tsdlv.session.sessions_view import SessionsView
from tsdlv.session.session_file_view import SessionFileView
from tsdlv.session.iterations_view import IterationsView

class FlaskApp:
  def __init__(self, name):
    self.flask_app = Flask(name)
    # enable CORS
    self.flask_app.after_request(self._after_request)

    self._create_rules()

  def run(self):
    self.flask_app.run()

  def _after_request(self, resp):
    h = resp.headers
    # prepare headers for CORS authentication
    h['Access-Control-Allow-Origin'] = '*'
    resp.headers = h

    print(resp.headers)

    return resp

  def _create_rules(self):
    self.flask_app.add_url_rule('/session/', view_func=SessionsView.as_view('sessions'))
    self.flask_app.add_url_rule('/session/<session_id>/file/', view_func=SessionFileView.as_view('session_files'))
    self.flask_app.add_url_rule('/session/<session_id>/file/<file_id>', view_func=IterationsView.as_view('file_iterations'))

if __name__ == '__main__':
  app = FlaskApp('tsdlv')
  app.run()