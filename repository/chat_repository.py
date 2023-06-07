from repository.chat_dto import ChatDTO
from repository.abstract_repository import AbstractRepository

class ChatRepository(AbstractRepository):
  def __init__(self):
    super().__init__(ChatDTO)

  def add(self, chat : ChatDTO):
    self._session.add(chat)
    self._session.flush()

    self._session.commit()

    return chat.id

  def update(self, id, chat : ChatDTO):
    current_chat = self.find(id)

    if current_chat is None:
      raise IndexError("Chat not found")
    
    current_chat.name = chat.name
    current_chat.description = chat.description
    current_chat.max_users = chat.max_users

    self._session.commit()