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

  def post(self):
    body = request.get_json()

    try:
      user = UserVO()
      user.fromJson(body)
      self.__user_service.add_user(user)
    except ValueError as e:
      abort(400, e)
    except Exception as e:
      abort(409, e)

    return jsonify(success="User created successfully!")

@ns.route("/me")
class UserTokenEndpoint(Resource):
  __user_service = UserService()

  def get(self):
    body = request.get_json()

    # Remover esta linha e arrumar os puts
    print(request.headers.get('Authorization'))

    try:
      user = UserVO()
      user.from_json_password_email(body)
      token = self.__user_service.get_token(user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)
    except Exception as e:
      abort(401, e)

    return jsonify(token=token)

@ns.route("/<int:id>")
class UserEndpoint(Resource):
  __user_service = UserService()

  def get(self, id):
    if id < 1:
      abort(403, "Invalid ID")

    try:
      user = self.__user_service.find_user(id)
    except IndexError as e:
      abort(404, e)

    return user.to_json()

  def put(self, id):
    if id < 1:
      abort(403, "Invalid ID")
      
    body = request.get_json()

    try:
      user = UserVO()
      user.fromJson(body)
      self.__user_service.update(id, user)
    except ValueError as e:
      abort(400, e)
    except IndexError as e:
      abort(404, e)

    return jsonify(success="User changed successfully")

  def delete(self, id):
    if id < 1:
      abort(403, "Invalid ID")

    try:
      self.__user_service.delete_user(id)
    except IndexError as e:
      abort(404, e)

    return jsonify(success="User deleted successfully")