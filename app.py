from flask import Flask, jsonify
from flask_restx import Api
from werkzeug.exceptions import HTTPException

from endpoints.user_endpoint import ns as user_ns
from endpoints.chat_endpoint import ns as chat_ns
from endpoints.message_endpoint import ns as message_ns

app = Flask(__name__)
api = Api(
  app,
  doc="/_docs",
  version="1.0.0",
  title="Chat api",
  description="Test chat api"
)

api.add_namespace(user_ns)
api.add_namespace(chat_ns)
api.add_namespace(message_ns)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), e.code

if __name__ == "__main__":
  app.run(debug=True)