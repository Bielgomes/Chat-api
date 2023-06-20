import communs
from flask import request, abort, jsonify, send_file
from flask_restx import Resource, Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage

from endpoints.abstract_endpoints import AbstractEndpoints
from endpoints.user_vo import UserVO

ns = Namespace("users", description="Endpoint para gerenciar usuários no Chat API")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

chat_model = ns.model('chat',
{
  "id": fields.Integer(required=True, description="Chat Id"),
  "name": fields.String(required=True, description="Chat Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="Chat Description", validate=lambda val: len(val) <= 140),
  "max_user": fields.Integer(required=True, description="Chat max users", validate=lambda val: val >= 2 and val <= 50),
})

user_register_model = ns.model('user_registry', {
  "email": fields.String(required=True, description="User Email", validate=lambda val: len(val) <= 320),
  "password": fields.String(required=True, description="User passwd", validate=lambda val: len(val) <= 30),
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
})

user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
})

user_info_model = ns.model('user_info', {
  "name": fields.String(required=True, description="User Name", validate=lambda val: len(val) <= 25),
  "description": fields.String(required=True, description="User Description", validate=lambda val: len(val) <= 140),
})

user_password_model = ns.model('user_password', {
  "password": fields.String(required=True, description="User passwd", validate=lambda val: len(val) <= 30)
})

user_email_model = ns.model('user_email', {
  "email": fields.String(required=True, description="User Email", validate=lambda val: len(val) <= 320)
})

user_login_model = ns.model('user_login', {
  "email": fields.String(required=True, description="User Email", validate=lambda val: len(val) <= 320),
  "password": fields.String(required=True, description="User passwd", validate=lambda val: len(val) <= 30)
})

@ns.route("")
class UsersEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success", user_model)
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self):
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

    user = self._user_service.find_user_by_id(id)
    return user.to_json()

  @ns.expect(user_register_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(409, "Conflict")
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

  @ns.doc(security="token")
  @ns.expect(user_info_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(404, "Not Found")
  def patch(self):
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
      user = UserVO()
      user.from_json_info(body)
      self._user_service.update_info(user, id)
    except ValueError as e:
      abort(400, str(e))

    return jsonify(success="User changed successfully")

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(401, "Unauthorized")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def delete(self):
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
      user = UserVO()
      user.from_json_login(body)
      self._user_service.delete_user(user)
      self.remove_from_cache(token, id)
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(401, str(e))

    return jsonify(success="User deleted successfully")
  
@ns.route("/<int:user_id>")
class UserEndpoint(Resource, AbstractEndpoints):

  @ns.response(200, "Success", user_model)
  @ns.response(400, "Bad Request")
  @ns.response(404, "Not Found")
  def get(self, user_id):
    if user_id < 1:
      abort(400, "Invalid Id")

    try:
      user = self._user_service.find_user_by_id(user_id)
    except IndexError as e:
      abort(404, str(e))

    return user.to_json()

@ns.route("/chats")
class UserChatsEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success", [chat_model])
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self):
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

    chats = self._user_service.find_chats(id)
    chats_json = communs._to_json(chats)

    return chats_json

@ns.route("/token")
class UserTokenEndpoint(Resource, AbstractEndpoints):

  @ns.expect(user_login_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(401, "Unauthorized")
  @ns.response(404, "Not Found")
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

  @ns.doc(security="token")
  @ns.expect(user_email_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  @ns.response(409, "Conflict")
  def patch(self):
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
      user = UserVO()
      user.from_json_email(body)
      self._user_service.update_email(user, id)
    except ValueError as e:
      abort(400, str(e))
    except Exception as e:
      abort(409, str(e))
    
    return jsonify(success="Email changed successfully")

@ns.route("/password")
class UserPasswordEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.expect(user_password_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def patch(self):
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
      user = UserVO()
      user.from_json_password(body)
      new_token = self._user_service.update_password(user, id)
      self.remove_from_cache(token, id)
      self.add_to_cache(new_token, id)
    except ValueError as e:
      abort(400, str(e))

    return jsonify(success="Password changed successfully")

@ns.route("/<int:user_id>/avatar")
class UserAvatarEndpoint(Resource, AbstractEndpoints):

  @ns.response(200, "Success", mimetype="image/jpeg", headers={"Content-Disposition": "inline; filename=avatar.jpg"})
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self, user_id):
    if user_id < 1:
      abort(403, "Invalid Id")

    try:
      self._user_service.find_user_by_id(user_id)
      filename = self._user_service.find_file(str(user_id))
      return send_file(filename, mimetype="image/jpeg", download_name="avatar.jpg")
    except IndexError or FileNotFoundError as e:
      abort(404, str(e))

@ns.route("/avatar")
class UserAvatarEndpoints(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.expect(upload_parser)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  @ns.response(413, "Payload Too Large")
  def post(self):
    token = request.headers.get("Authorization")
    if token is None or not len(token) >= 19:
      abort(403, "Invalid Token")

    id = self.get_id_from_cache(token)

    if not id:
      try:
        user = self._user_service.find_user(token)
        id = user.id
        self.add_to_cache(token, id)
      except IndexError as e:
        abort(404, str(e))

    if "file" not in request.files:
      abort(400, "The avatar is required")

    file = request.files["file"]
    if file.filename.strip() == '' or not communs._allowed_file(file.filename):
      abort(400, f'invalid file, extension files are allowed {communs.ALLOWED_EXTENSIONS}')

    blob = file.read()
    if len(blob) == 0 or len(blob) / (1024 * 1024) > 16:
      abort(413, 'invalid file size (Max. 16mb)')

    self._user_service.save_file(file, blob, id)
    
    return jsonify(success="User avatar has been successfully added!")