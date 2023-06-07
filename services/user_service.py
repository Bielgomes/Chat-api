import bcrypt
from uuid import uuid4

from repository.user_repository import UserRepository
from repository.user_dto import UserDTO
from endpoints.user_vo import UserVO

class UserService:
  __user_repository = UserRepository()

  def get_token(self, user):
    current_user = self.__user_repository.find_by_email(user.email)
    if not current_user:
      raise IndexError("User not exists")

    if not current_user.email == user.email or not bcrypt.checkpw(user.password.encode("utf-8"), current_user.password.encode("utf-8")):
        raise Exception("Invalid Credentials")
    
    return self.__user_repository.get_token(current_user.id)[0]

  def find_user(self, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if user is None:
      raise IndexError("User not found")
    
    return UserVO.from_dto(user)

  def add_user(self, user : UserVO):
    if self.__user_repository.find_by_email(user.email):
      raise Exception("This email is already registered")
    
    userDTO = user.to_dto()

    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    userDTO.token = str(uuid4())

    self.__user_repository.add(userDTO)

  def update_info(self, token, user : UserVO):
    self.__user_repository.update_info(token, user.to_dto())

  def update_email(self, token, user : UserVO):
    current_user = self.__user_repository.find_by_email(user.email)
    if current_user:
      raise Exception("This email is already registered")

    self.__user_repository.update_email(token, user.to_dto())

  def update_password(self, token, user : UserVO):
    userDTO = user.to_dto()

    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    userDTO.token = str(uuid4())

    self.__user_repository.update_password(token, userDTO)

  def delete_user(self, user : UserVO):
    current_user = self.__user_repository.find_by_email(user.email)
    if current_user is None:
      raise IndexError("User not found!")
    
    if not current_user.email == user.email or not bcrypt.checkpw(user.password.encode("utf-8"), current_user.password.encode("utf-8")):
        raise Exception("Invalid Credentials")
    
    self.__user_repository.delete(current_user)
