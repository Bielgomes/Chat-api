from services.user_service import UserService
from services.chat_service import ChatService
from services.message_service import MessageService

class AbstractEndpoints():
  _user_service = UserService()
  _chat_service = ChatService()
  _message_service = MessageService()
  _token_cache = {}

  def add_to_cache(self, token, id):
    self._token_cache[token] = id

  def search_in_cache(self, token, id):
    if self._token_cache[token] == id:
      return self._token_cache[token]

  def remove_from_cache(self, token, id):
    if self._token_cache[token] == id:
      del self._token_cache[token]

  def get_id(self, token):
    return self._token_cache[token]          