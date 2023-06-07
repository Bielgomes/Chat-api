from repository.user_chat_dto import UserChatDTO
from repository.abstract_repository import AbstractRepository

class UserChatRepository(AbstractRepository):
  def __init__(self):
    super().__init__(UserChatDTO)

  def find_by_user_and_chat(self, id_user, id_chat):
    return self._session.query(self._class).filter(self._class.id_user == id_user, self._class.id_chat == id_chat).first()