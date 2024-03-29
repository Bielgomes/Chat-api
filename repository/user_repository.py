from repository.abstract_repository import AbstractRepository
from repository.user_dto import UserDTO

class UserRepository(AbstractRepository):
  def __init__(self):
    super().__init__(UserDTO)

  def add(self, user: UserDTO, password):
    self._session.add(user)
    self._session.flush()

    user.token = str(hash(f"{user.id}.{password}"))

    self._session.commit()

    return user.token, user.id
  
  def find_by_ids(self, ids):
    return self._session.query(self._class).filter(self._class.id.in_(ids)).all()

  def find_by_token(self, token):
    return self._session.query(self._class).filter(self._class.token == token).first()
  
  def find_by_email(self, email):
    return self._session.query(self._class).filter(self._class.email == email).first()

  def get_token(self, id):
    return self._session.query(self._class.token).filter(self._class.id == id).first()

  def update_info(self, id, user : UserDTO):
    current_user = self.find(id)

    current_user.name = user.name
    current_user.description = user.description

    self._session.commit()

  def update_email(self, id, user : UserDTO):
    current_user = self.find(id)

    current_user.email = user.email

    self._session.commit()

  def update_password(self, id, user : UserDTO, new_password):
    current_user = self.find(id)
    
    current_user.password = user.password
    current_user.token = str(hash(f"{current_user.id}.{new_password}"))

    self._session.commit()

    return current_user.token