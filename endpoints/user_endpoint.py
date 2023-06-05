from flask import request, abort, jsonify
from flask_restx import Resource, Namespace, fields
from endpoints.user_vo import UserVO
from services.user_service import UserService

ns = Namespace("users", description="Chat API")

user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "email": fields.String(required=True, description="User Email"),
  "password": fields.String(required=True, description="User passwd"),
  "token": fields.String(required=True, description="Validation Token")
})

@ns.route("")
class UsersEndpoint(Resource):
  __user_service = UserService()

  def get(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    try:
      user = self.__user_service.find_user(token)
    except IndexError as e:
      abort(404, e)

    return user.to_json()
  
  def post(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json(body)
      self.__user_service.add_user(user)
    except ValueError as e:
      abort(400, e)
    except Exception as e:
      abort(409, e)

    return jsonify(success="User created successfully!")

  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")
      
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_info(body)
      self.__user_service.update_info(token, user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)

    return jsonify(success="User changed successfully")

  def delete(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_login(body)
      self.__user_service.delete_user(user)
    except IndexError as e:
      abort(404, e)

    return jsonify(success="User deleted successfully")

@ns.route("/token")
class UserTokenEndpoint(Resource):
  __user_service = UserService()

  def get(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_login(body)
      token = self.__user_service.get_token(user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(401, e)

    return jsonify(token=token)

@ns.route("/email")
class UserEmailEndpoint(Resource):
  __user_service = UserService()
  
  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()
    try:
      user = UserVO()
      user.from_json_email(body)
      self.__user_service.update_email(token, user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(409, e)
    
    return jsonify(success="Email changed successfully")

@ns.route("/password")
class UserPasswordEndpoint(Resource):
  __user_service = UserService()

  def patch(self):
    token = request.headers.get('Authorization')
    if token is None or not len(token) == 36:
      abort(403, "Invalid Token")

    body = request.get_json()

    try:
      user = UserVO()
      user.from_json_password(body)
      self.__user_service.update_password(token, user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)

    return jsonify(success="Password changed successfully")

    

    

