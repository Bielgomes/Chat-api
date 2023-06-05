from repository.user_chat_dto import UserChatDTO
from repository.abstract_repository import AbstractRepository

class UserRepository(AbstractRepository):
    def __init__(self):
        super().__init__(UserChatDTO)