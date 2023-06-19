import bcrypt
import os

from endpoints.user_vo import UserVO
from endpoints.chat_vo import ChatVO

from repository.user_dto import UserDTO

from repository.user_repository import UserRepository
from repository.chat_repository import ChatRepository
from repository.message_repository import MessageRepository
from repository.user_chat_repository import UserChatRepository

class UserService:
  def __init__(self):
    self.__STORAGE_PATH = os.path.join(os.getcwd(), 'tmp\\avatares')

    self.__user_repository = UserRepository()
    self.__chat_repository = ChatRepository()
    self.__message_repository = MessageRepository()
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
  
  def find_user_by_id(self, id):
    user : UserDTO = self.__user_repository.find(id)
    if user is None:
      raise IndexError("User not found")

    return UserVO.from_dto(user)
  
  def find_chats(self, id):
    user : UserDTO = self.__user_repository.find(id)
    
    dtos = self.__user_chat_repository.find_by_user(user.id)
    chat_ids = [dto.id_chat for dto in dtos]

    dtos = self.__chat_repository.find_by_ids(chat_ids)

    return [ChatVO.from_dto(dto) for dto in dtos]

  def find_file(self, name):
    for path, _, files in os.walk(self.__STORAGE_PATH): 
      for filename in files:
        if name in filename:
          return os.path.join(path, filename)
    raise FileNotFoundError('File not found')

  def save_file(self, file, blob, id):
    filename = f"{id}.{file.filename.split('.')[-1]}"
    file_image = open(os.path.join(self.__STORAGE_PATH, filename), 'wb')
    file_image.write(blob)
    file_image.close()

  def add_user(self, user : UserVO):
    if self.__user_repository.find_by_email(user.email):
      raise Exception("This email is already registered")
    
    userDTO = user.to_dto()
    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    return self.__user_repository.add(userDTO)

  def update_info(self, user : UserVO, id):
    self.__user_repository.update_info(id, user.to_dto())

  def update_email(self, newUser : UserVO, id):
    user : UserDTO = self.__user_repository.find(id)
    if self.__user_repository.find_by_token(newUser.email):
      raise Exception("This email is already registered")

    self.__user_repository.update_email(user.id, newUser.to_dto())

  def update_password(self, newUser : UserVO, id):
    userDTO = newUser.to_dto()
    userDTO.password = bcrypt.hashpw(userDTO.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    self.__user_repository.update_password(id, userDTO)

  def delete_user(self, user : UserVO):
    current_user : UserDTO = self.__user_repository.find_by_email(user.email)
    if not current_user.email == user.email or not bcrypt.checkpw(user.password.encode("utf-8"), current_user.password.encode("utf-8")):
      raise Exception("Invalid Credentials")

    chats = self.__chat_repository.find_by_owner(current_user.id)
    chats_ids = [chat.id for chat in chats]

    self.__user_chat_repository.delete_by_user(current_user.id)
    
    #self.__user_chat_repository.delete_by_chats(chats_ids)

    self.__message_repository.delete_by_chats(chats_ids)
    self.__chat_repository.delete_by_owner(current_user.id)
    self.__user_repository.delete(current_user)

    return current_user.id