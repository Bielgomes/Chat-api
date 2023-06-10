from repository.message_dto import MessageDTO
from repository.abstract_repository import AbstractRepository

class MessageRepository(AbstractRepository):
  def __init__(self):
    super().__init__(MessageDTO)

  def find_all_by_chat(self, chat_id):
    return self._session.query(self._class).filter(self._class.id_chat == chat_id).all()
  
  def delete_by_chat(self, chat_id):
    self._session.query(self._class).filter(self._class.id_chat == chat_id).delete()
    self._session.commit()