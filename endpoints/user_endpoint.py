from flask import request, abort, jsonify
from flask_restx import Resource, Namespace, fields
from endpoints.user_vo import UserVO
from services.user_service import UserService
import communs

ns = Namespace("user", " description='The IMDb ns is an interface that enables developers to access and utilize the extensive movie and TV show database provided by IMDb (Internet Movie Database). With the IMDb ns, developers can retrieve detailed information about films, television series, actors, and other related content. This includes data such as titles, release dates, genres, ratings, cast and crew details, plot summaries, images, and more. By integrating the IMDb ns into their applications, developers can enhance their services with comprehensive movie and TV show information, enabling features like search functionality, personalized recommendations, and rich media experiences. The IMDb ns empowers developers to create engaging entertainment-related applications that leverage the wealth of data available in the IMDb database, providing users with valuable insights and an enhanced viewing experience.")

user_model = ns.model('user', {
  "id": fields.Integer(required=True, description="User Id"),
  "email": fields.String(required=True, description="User Email"),
  "password": fields.String(required=True, description="User passwd"),
  "token": fields.String(required=True, description="Validation Token")
})

@ns.route("")
class UserEndpoint(Resource):
  _user_service = UserService()

@ns.route("/<int:id>")
class UserEndpointGet(Resource):
  _user_service = UserService()

  def get(self, id):
    if id < 1:
      abort(403, "Invalid ID")

    try:
      user = self._user_service.find_user(id)
    except IndexError as e:
      abort(404, str(e))

    return user.to_json()