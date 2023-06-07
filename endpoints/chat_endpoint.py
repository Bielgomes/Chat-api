from flask import request, jsonify, abort
from flask_restx import Resource, Namespace, fields
from endpoints.chat_vo import ChatVO
from services.chat_service import ChatService

ns = Namespace("chats", description='Chat API')

chat_model = ns.model('chat',
{
    "id": fields.Integer(required=True, description="Chat Id"),
    "name": fields.String(required=True, description="Chat Name", validate=lambda val: len(val) <= 25),
    "description": fields.String(required=True, description="Chat Description", validate=lambda val: len(val) <= 140),
    "max_user": fields.Integer(required=True, description="Chat max users", validate=lambda val: val >= 2 and val <= 50),
})

@ns.route("")
class ChatsEndpoint(Resource):
  __chat_service = ChatService()

  def post(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()

    try:
      chat = ChatVO()
      chat.from_json(body)
      self.__chat_service.create_chat(chat, token)
    except ValueError as e:
      abort(400, e)
    except Exception as e:
      abort(409, e)
      
    return jsonify(success="Chat created successfully!")

@ns.route("/<int:chat_id>")
class ChatEndpoint(Resource):
  __chat_service = ChatService()

  def get(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    try:
      chat = self.__chat_service.find_chat(chat_id, token)
    except IndexError as e:
      abort(404, str(e))

    return chat.to_json()

  def put(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()

    try:
      chat = ChatVO()
      chat.from_json(body)
      self.__chat_service.update(chat_id, chat, token)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(403, e)

    return jsonify(success="Chat updated successfully!")

  def delete(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")
    
    try:
      self.__chat_service.remove_chat(chat_id, token)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(403, e)

    return jsonify(success="Chat removed successfully!")

@ns.route("/<int:chat_id>/join")
class ChatJoinEndpoint(Resource):
  __chat_service = ChatService()

  def post(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")
    
    try:
      self.__chat_service.join_chat(chat_id, token)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(403, e)

    return jsonify(success="Chat joined successfully!")