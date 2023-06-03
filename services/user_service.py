from repository.user_repository import UserRepository
from repository.user_dto import UserDTO
from endpoints.user_vo import UserVO

from uuid import uuid4

class UserService():
  __user_repository = UserRepository()

  def get_token(self, user):
    current_user = self.__user_repository.find_by_email(user.email)
    if not current_user:
      raise IndexError("User not exists")

    if not current_user.email == user.email and not current_user.password == user.password:
      raise Exception("Invalid Credentials")

    return self.__user_repository.get_token(current_user.id)[0]

  def find_user(self, id):
    user : UserDTO = self.__user_repository.find(id)
    if user is None:
      raise IndexError("User not found")
    
    return UserVO.from_dto(user)

  def add_user(self, user : UserVO):
    if self.__user_repository.find_by_email(user.email):
      raise Exception("This email is already registered")
    
    userDTO = user.to_dto()
    userDTO.token = str(uuid4())

    self.__user_repository.add(userDTO)

  def delete_user(self, id):
    user = self.__user_repository.find(id)
    if user is None:
      raise IndexError("User not found!")
    
    self.__user_repository.delete(user)

  def update(self, id, user:UserVO):
    self.__user_repository.update(id, user.to_dto())
