from repository.abstract_repository import AbstractRepository
from repository.user_dto import UserDTO

class UserRepository(AbstractRepository):
  def __init__(self):
    super().__init__(UserDTO)

  def finb_by_token(self, token):
    return self._session.query(self._class).filter(self._class.token == token).first()
  
  def find_by_email(self, email):
    return self._session.query(self._class).filter(self._class.email == email).first()

  def get_token(self, id):
    return self._session.query(self._class.token).filter(self._class.id == id).first()

  def update_info(self, token, user : UserDTO):
    current_user = self.finb_by_token(token)

    if current_user is None:
      raise IndexError("User not found!")

    current_user.name = user.name
    current_user.description = user.description

    self._session.commit()

  def update_email(self, token, user : UserDTO):
    current_user = self.finb_by_token(token)

    if current_user is None:
      raise IndexError("User not found!")

    current_user.email = user.email

    self._session.commit()

  def update_password(self, token, user : UserDTO):
    current_user = self.finb_by_token(token)

    if current_user is None:
      raise IndexError("User not found!")
    
    current_user.password = user.password
    current_user.token = user.token

    self._session.commit()