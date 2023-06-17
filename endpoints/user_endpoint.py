import communs
from flask import request, abort, jsonify
from flask_restx import Resource, Namespace, fields

from endpoints.abstract_endpoints import AbstractEndpoints

from endpoints.user_vo import UserVO

ns = Namespace("users", description="Chat API")

registry_user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "email": fields.String(required=True, description="User Email"),
  "password": fields.String(required=True, description="User passwd"),
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
  "token": fields.String(required=True, description="Validation Token")
})

user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
})

@ns.route("")
class UsersEndpoint(Resource, AbstractEndpoints):
  def __init__(self):
    super().__init__()

  def get(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    try:
      # FOFO
      self._user_service.verify_token(token)

      user = self._user_service.find_user(token)
    except IndexError as e:
      abort(404, str(e))

    return user.to_json()
  
  def post(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json(body)
      token, id = self._user_service.add_user(user)
      self.add_to_cache(token, id)
    except ValueError as e:
      abort(400, str(e))
    except Exception as e:
      abort(409, str(e))

    return jsonify(success="User created successfully!")

  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")
      
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_info(body)
      self._user_service.update_info(token, user)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))

    return jsonify(success="User changed successfully")

  def delete(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    id = self.get_id(token)

    if not id:
      try:
        id = self._user_service.find_user(token).id
      except IndexError as e:
        abort(404, str(e))
  
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_login(body)
      self._user_service.delete_user(user)
      self.remove_from_cache(token, id)
      
    except IndexError as e:
      abort(404, str(e))

    return jsonify(success="User deleted successfully")

@ns.route("/chats")
class UserChatsEndpoint(Resource, AbstractEndpoints):
  def get(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    try:
      chats = self._user_service.find_chats(token)
      chats = communs._to_json(chats)
    except IndexError as e:
      abort(404, str(e))

    return chats

@ns.route("/token")
class UserTokenEndpoint(Resource, AbstractEndpoints):
  def post(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_login(body)
      token = self._user_service.get_token(user)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(401, str(e))

    return jsonify(token=token)

@ns.route("/email")
class UserEmailEndpoint(Resource, AbstractEndpoints):  
  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()
    try:
      user = UserVO()
      user.from_json_email(body)
      self._user_service.update_email(token, user)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(409, str(e))
    
    return jsonify(success="Email changed successfully")

@ns.route("/password")
class UserPasswordEndpoint(Resource, AbstractEndpoints):
  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_password(body)
      self._user_service.update_password(token, user)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))

    return jsonify(success="Password changed successfully")