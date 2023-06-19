from datetime import datetime

from endpoints.message_vo import MessageVO

from repository.message_repository import MessageRepository
from repository.user_repository import UserRepository
from repository.chat_repository import ChatRepository
from repository.user_chat_repository import UserChatRepository

from repository.message_dto import MessageDTO
from repository.user_dto import UserDTO
from repository.chat_dto import ChatDTO


class MessageService:
  def __init__(self):
    self.__message_repository = MessageRepository()
    self.__user_repository = UserRepository()
    self.__chat_repository = ChatRepository()
    self.__user_chat_repository = UserChatRepository()

  def find_all_messages_from_chat(self, chat_id, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    chat : ChatDTO = self.__chat_repository.find(chat_id)
    if chat is None:
      raise IndexError("Chat not found")
    
    if self.__user_chat_repository.find_by_user_and_chat(user.id, chat_id) is None:
      raise Exception("User not in this chat") 
    
    dtos = self.__message_repository.find_all_by_chat(chat_id)

    return [MessageVO.from_dto(dto) for dto in dtos]

  def add_message(self, chat_id, message : MessageVO, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    chat : ChatDTO = self.__chat_repository.find(chat_id)
    if chat is None:
      raise IndexError("Chat not found")
    
    if self.__user_chat_repository.find_by_user_and_chat(user.id, chat_id) is None:
      raise Exception("User not in this chat") 

    message.id_user = user.id
    message.id_chat = chat_id
    message.date = datetime.now()

    self.__message_repository.add(message.to_dto())

  def remove_message(self, chat_id, message_id, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    chat : ChatDTO = self.__chat_repository.find(chat_id)
    if chat is None:
      raise IndexError("Chat not found")
    
    if self.__user_chat_repository.find_by_user_and_chat(user.id, chat_id) is None:
      raise Exception("User not in this chat") 
    
    message : MessageDTO = self.__message_repository.find(message_id)
    if message is None:
      raise IndexError("Message not found") 
    
    if message.id_user != user.id:
      raise PermissionError("This user does not own this message")
    
    self.__message_repository.delete(message)