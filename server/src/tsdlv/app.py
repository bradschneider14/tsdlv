from flask import Flask
from tsdlv.session.sessions_view import SessionsView
from tsdlv.session.session_file_view import SessionFileView

class FlaskApp:
  def __init__(self, name):
    self.flask_app = Flask(name)
    self._create_rules()

  def run(self):
    self.flask_app.run()

  def _create_rules(self):
    self.flask_app.add_url_rule('/session/', view_func=SessionsView.as_view('sessions'))
    self.flask_app.add_url_rule('/session/<session_id>/file/', view_func=SessionFileView.as_view('session_files'))

if __name__ == '__main__':
  app = FlaskApp('tsdlv')
  app.run()