from repository.abstract_repository import AbstractRepository
from repository.user_dto import UserDTO

class UserRepository(AbstractRepository):
    def __init__(self):
        super().__init__(UserDTO)