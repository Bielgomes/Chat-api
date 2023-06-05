from repository.message_dto import MessageDTO
from repository.abstract_repository import AbstractRepository

class MessageRepository(AbstractRepository):
  def __init__(self):
    super().__init__(MessageDTO)