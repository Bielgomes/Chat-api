from flask import Flask, jsonify
from flask_restx import Api

from endpoints.user_endpoint import ns as user_ns

app = Flask(__name__)
api = Api(
  app,
  doc="/_docs",
  version="1.0.0",
  title="Chat api",
  description="Test chat api"
)

api.add_namespace(user_ns)

@app.errorhandler(403)
def _forbidden(e):
  return jsonify(error=str(e)), 403

@app.errorhandler(404)
def _not_found(e):
  return jsonify(error=str(e)), 404

if __name__ == "__main__":
  app.run(debug=True)