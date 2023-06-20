from flask import Flask
from flask_restx import Api

from endpoints.user_endpoint import ns as user_ns
from endpoints.chat_endpoint import ns as chat_ns
from endpoints.message_endpoint import ns as message_ns

app = Flask(__name__)
api = Api(
  app,
  authorizations={
    "token": {
      "type": "apiKey",
      "in": "header",
      "name": "Authorization"
    }
  },
  doc="/_docs",
  version="1.0.0",
  title="Chat api",
  description="Uma API de chat que permite gerenciar usuários, chats e mensagens."
)

api.add_namespace(user_ns)
api.add_namespace(chat_ns)
api.add_namespace(message_ns)

if __name__ == "__main__":
  app.run(debug=True)