import communs 
from flask import request, abort, jsonify
from flask_restx import Resource, Namespace, fields

from endpoints.abstract_endpoints import AbstractEndpoints

from endpoints.message_vo import MessageVO

ns = Namespace("chats", description="Chat API")

message_model = ns.model("message",
{
  "id": fields.Integer(required=True, description="Message Id"),
  "id_user": fields.Integer(required=True, description="User Id"),
  "id_chat": fields.Integer(required=True, description="Chat Id"),
  "date": fields.DateTime(required=True, description="Date"),
  "message": fields.String(required=True, description="Message", validate=lambda val: len(val) <= 400)
})

message_register_model = ns.model("message_register",
{
  "message": fields.String(required=True, description="Message", validate=lambda val: len(val) <= 400)
})

messages_model = [message_model]

@ns.route("/<int:chat_id>/messages")
class MessagesEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token", params={'userid': 'User Id', 'text': 'Text'})
  @ns.response(200, "Success", messages_model)
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def get(self, chat_id):
    userid = request.args.get('userid')
    text = request.args.get('text')

    token = request.headers.get('Authorization')
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
    try:
      messages = self._message_service.find_all_messages_from_chat(chat_id, id)
      messages = communs._to_json(messages)
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(403, str(e))

    if userid:
      messages = [message for message in messages if message['id_user'] == int(userid)]

    if text:
      messages = [message for message in messages if text.lower() in message.get('message', '').lower()]

    return messages

  @ns.doc(security="token")
  @ns.expect(message_register_model, validate=True)
  @ns.response(200, "Success")
  @ns.response(400, "Bad Request")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def post(self, chat_id):
    token = request.headers.get('Authorization')
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
      
    body = request.get_json()

    try:
      message = MessageVO()
      message.from_json(body)
      self._message_service.add_message(chat_id, message, id)
    except ValueError as e:
      abort(400, str(e))
    except IndexError as e:
      abort(404, str(e))
    except Exception as e:
      abort(403, str(e))

    return jsonify(success="Message created successfully")

@ns.route("/<int:chat_id>/messages/<int:message_id>")
class MessageEndpoint(Resource, AbstractEndpoints):

  @ns.doc(security="token")
  @ns.response(200, "Success")
  @ns.response(401, "Unauthorized")
  @ns.response(403, "Forbidden")
  @ns.response(404, "Not Found")
  def delete(self, chat_id, message_id):
    token = request.headers.get('Authorization')
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

    try:
      self._message_service.remove_message(chat_id, message_id, id)
    except IndexError as e:
      abort(404, str(e))
    except PermissionError as e:
      abort(401, str(e))
    except Exception as e:
      abort(403, str(e))

    return jsonify(success="Message deleted successfully")