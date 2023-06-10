import bcrypt
from uuid import uuid4

from endpoints.user_vo import UserVO
from endpoints.chat_vo import ChatVO

from repository.user_dto import UserDTO

from repository.user_repository import UserRepository
from repository.chat_repository import ChatRepository
from repository.user_chat_repository import UserChatRepository

class UserService:
  def __init__(self):
    self.__user_repository = UserRepository()
    self.__chat_repository = ChatRepository()
    self.__user_chat_repository = UserChatRepository()

  def get_token(self, user):
    current_user : UserDTO = self.__user_repository.find_by_email(user.email)
    if current_user is None:
      raise IndexError("User not found")

    if not current_user.email == user.email or not bcrypt.checkpw(user.password.encode("utf-8"), current_user.password.encode("utf-8")):
        raise Exception("Invalid Credentials")
    
    return self.__user_repository.get_token(current_user.id)[0]

  def find_user(self, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if user is None:
      raise IndexError("User not found")
    
    return UserVO.from_dto(user)
  
  def find_chats(self, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if user is None:
      raise IndexError("User not found")
    
    dtos = self.__user_chat_repository.find_by_user(user.id)
    chat_ids = [dto.id_chat for dto in dtos]

    dtos = self.__chat_repository.find_by_ids(chat_ids)

    return [ChatVO.from_dto(dto) for dto in dtos]

  def add_user(self, user : UserVO):
    if self.__user_repository.find_by_email(user.email):
      raise Exception("This email is already registered")
    
    userDTO = user.to_dto()

    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    userDTO.token = str(uuid4())

    self.__user_repository.add(userDTO)

  def update_info(self, token, user : UserVO):
    current_user : UserDTO = self.__user_repository.find_by_token(token)
    if current_user is None:
      raise IndexError("User not found!")
    
    self.__user_repository.update_info(token, user.to_dto())

  def update_email(self, token, newUser : UserVO):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if user is None:
      raise IndexError("User not found!")
  
    if self.__user_repository.find_by_token(newUser.email):
      raise Exception("This email is already registered")

    self.__user_repository.update_email(user.id, newUser.to_dto())

  def update_password(self, token, newUser : UserVO):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if user is None:
      raise IndexError("User not found!")

    userDTO = newUser.to_dto()

    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    userDTO.token = str(uuid4())

    self.__user_repository.update_password(token, userDTO)

  def delete_user(self, user : UserVO):
    current_user : UserDTO = self.__user_repository.find_by_email(user.email)
    if current_user is None:
      raise IndexError("User not found!")
    
    if not current_user.email == user.email or not bcrypt.checkpw(user.password.encode("utf-8"), current_user.password.encode("utf-8")):
        raise Exception("Invalid Credentials")
    
    self.__user_repository.delete(current_user)
