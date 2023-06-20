from repository.user_chat_dto import UserChatDTO
from repository.abstract_repository import AbstractRepository

class UserChatRepository(AbstractRepository):
  def __init__(self):
    super().__init__(UserChatDTO)

  def find_by_user_and_chat(self, id_user, id_chat):
    return self._session.query(self._class).filter(self._class.id_user == id_user, self._class.id_chat == id_chat).first()
  
  def find_by_user(self, id_user):
    return self._session.query(self._class).filter(self._class.id_user == id_user).all()
  
  def find_by_chat(self, id_chat):
    return self._session.query(self._class).filter(self._class.id_chat == id_chat).all()
  
  def delete_by_user(self, id_user):
    ids = self._session.query(self._class).filter(self._class.id_user == id_user).all()
    self._session.query(self._class).filter(self._class.id_user == id_user).delete()
    
    self._session.commit()

    return ids
  
  def delete_by_chat(self, id_chat):
    self._session.query(self._class).filter(self._class.id_chat == id_chat).delete()
    self._session.commit()

  def delete_by_chats(self, chat_ids):
    self._session.query(self._class).filter(self._class.id_chat.in_(chat_ids)).delete()
    self._session.commit()

  def remove_by_user_and_chat(self, user_id, chat_id):
    self._session.query(self._class).filter(self._class.id_user == user_id, self._class.id_chat == chat_id).delete()
    self._session.commit()