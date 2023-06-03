from repository.abstract_repository import AbstractRepository
from repository.user_dto import UserDTO

class UserRepository(AbstractRepository):
  def __init__(self):
    super().__init__(UserDTO)

  def update(self, id, user : UserDTO):
    current_user = self.find(id)

    current_user.name = user.name
    current_user.description = user.description

    self._session.commit()

  def find_by_email(self, email):
    return self._session.query(self._class).filter(self._class.email == email).first()

  def get_token(self, id):
    return self._session.query(self._class.token).filter(self._class.id == id).first()