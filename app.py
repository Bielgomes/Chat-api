from flask import Flask, jsonify
from flask_restx import Api

from endpoints.user_endpoint import ns as user_ns
from endpoints.chat_endpoint import ns as chat_ns

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

@app.errorhandler(400)
def _bad_request(e):
  return jsonify(error=str(e)), 400

@app.errorhandler(401)
def _unauthorized(e):
  return jsonify(error=str(e)), 401

@app.errorhandler(403)
def _forbidden(e):
  return jsonify(error=str(e)), 403

@app.errorhandler(404)
def _not_found(e):
  return jsonify(error=str(e)), 404

@app.errorhandler(409)
def _conflict(e):
  return jsonify(error=str(e)), 409

if __name__ == "__main__":
  app.run(debug=True)