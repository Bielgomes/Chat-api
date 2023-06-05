from repository.chat_dto import ChatDTO
from repository.abstract_repository import AbstractRepository

class ChatRepository(AbstractRepository):
  def __init__(self):
    super().__init__(ChatDTO)