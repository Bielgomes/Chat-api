from flask import request, jsonify, abort
from flask_restx import Resource, Namespace, fields

import communs

from endpoints.abstract_endpoints import AbstractEndpoints
from endpoints.chat_vo import ChatVO

ns = Namespace("chats", description='Endpoint para gerenciar chats no Chat API')

user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
})

chat_register_model = ns.model('chat_register',
{
  "name": fields.String(required=True, description="Chat Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="Chat Description", validate=lambda val: len(val) <= 140),
  "max_users": fields.Integer(required=True, description="Chat max users", validate=lambda val: val >= 2 and val <= 50),
})

chat_model = ns.model('chat',
{
  "id": fields.Integer(required=True, description="Chat Id"),
  "name": fields.String(required=True, description="Chat Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="Chat Description", validate=lambda val: len(val) <= 140),
  "max_users": fields.Integer(required=True, description="Chat max users", validate=lambda val: val >= 2 and val <= 50),
})

@ns.route("")
class ChatsEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.expect(chat_register_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(404, "Not Found")
  def post(self):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))

    body = request.get_json()

    try:
      chat = ChatVO()
      chat.from_json(body)
      self._chat_service.add_chat(chat, id)
    except ValueError as e:
      abort(400, str(e))

    return jsonify(success="Chat created successfully!")

@ns.route("/<int:chat_id>")
class ChatEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success", chat_model)
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    if chat_id < 1:
      abort(403, "Invalid Chat Id")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))

    try:
      chat = self._chat_service.find_chat(chat_id)
    except IndexError as e:
      abort(404, str(e))

    return chat.to_json()

  @ns.doc(security="token")
  @ns.expect(chat_register_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(401, "Unauthorized")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def put(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))

    body = request.get_json()

    try:
      chat = ChatVO()
      chat.from_json(body)
      self._chat_service.update(chat_id, chat, id)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))
    except PermissionError as e:
      abort(401, str(e))

    return jsonify(success="Chat updated successfully!")

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(401, "Unauthorized")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def delete(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))
    
    try:
      self._chat_service.remove_chat(chat_id, id)
    except IndexError as e:
      abort(404, str(e))
    except PermissionError as e:
      abort(401, str(e))

    return jsonify(success="Chat removed successfully!")

@ns.route("/<int:chat_id>/users")
class ChatUsersEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success", [user_model])
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    if chat_id < 1:
      abort(403, "Invalid Chat Id")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))
    
    try:
      users = self._chat_service.find_users(chat_id, id)
      users_json = communs._to_json(users)
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(403, str(e))

    return users_json

@ns.route("/<int:chat_id>/join")
class ChatJoinEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  @ns.response(409, "Conflict")
  def post(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    if chat_id < 1:
      abort(403, "Invalid Chat Id")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))
    
    try:
      self._chat_service.join_chat(chat_id, id)
    except IndexError as e:
      abort(404, str(e))
    except ValueError as e:
      abort(403, str(e))
    except Exception as e:
      abort(409, str(e))

    return jsonify(success="Chat joined successfully!")
  
@ns.route("/<int:chat_id>/leave")
class ChatJoinEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def delete(self, chat_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    if chat_id < 1:
      abort(403, "Invalid Chat Id")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))
        
    try:
      self._chat_service.leave_chat(chat_id, id)
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(403, str(e))

    return jsonify(success="Chat leave successfully!")
  
@ns.route("/<int:chat_id>/admin/users/<int:user_id>")
class ChatAdminEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(401, "Unauthorized")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def delete(self, chat_id, user_id):
    token = request.headers.get('Authorization')
    if token is None or not token.lstrip('-').isdigit():
      abort(403, "Invalid Token")

    if chat_id < 1:
      abort(403, "Invalid Chat Id")

    if user_id < 1:
      abort(403, "Invalid User Id")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))

    try:
      self._chat_service.admin_remove_user_from_chat(chat_id, user_id, id)
    except IndexError as e:
      abort(404, str(e))
    except PermissionError as e:
      abort(401, str(e))
    except Exception as e:
      abort(403, str(e))

    return jsonify(success="User removed successfully!")