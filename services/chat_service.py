from endpoints.chat_vo import ChatVO
from endpoints.user_vo import UserVO

from repository.chat_repository import ChatRepository
from repository.user_repository import UserRepository
from repository.message_repository import MessageRepository
from repository.user_chat_repository import UserChatRepository

from repository.user_dto import UserDTO
from repository.chat_dto import ChatDTO
from repository.user_chat_dto import UserChatDTO

class ChatService:
  def __init__(self):
    self.__message_repository = MessageRepository()
    self.__user_repository = UserRepository()
    self.__chat_repository = ChatRepository()
    self.__user_chat_repository = UserChatRepository()

  def find_chat(self, id):
    chat : ChatDTO = self.__chat_repository.find(id)
    if chat is None:
      raise IndexError("Chat not found")
    
    return ChatVO.from_dto(chat)
  
  def find_users(self, id):
    users = self.__user_chat_repository.find_by_chat(id)
    if users is None:
      raise IndexError("Chat not found")
    
    users_vo = [UserVO.from_dto(user) for user in users]
    
    return users_vo

  def add_chat(self, chat : ChatVO, user_id):
    user : UserDTO = self.__user_repository.find(user_id)

    chatDTO = chat.to_dto()
    chatDTO.id_owner = user.id

    userChatDTO = UserChatDTO()
    userChatDTO.id_user = user.id

    chat_id = self.__chat_repository.add(chatDTO)
    userChatDTO.id_chat = chat_id

    self.__user_chat_repository.add(userChatDTO)

  def join_chat(self, id, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    chat : ChatDTO = self.__chat_repository.find(id)
    if chat is None:
      raise IndexError("Chat not found")

    if self.__user_chat_repository.find_by_user_and_chat(user.id, chat.id):
      raise Exception("User already in this chat")
    
    users = self.__user_chat_repository.find_by_chat(chat.id)
    if chat.max_users <= len(users):
      raise ValueError("Chat is full")
    
    userChatDTO = UserChatDTO()
    userChatDTO.id_chat = chat.id
    userChatDTO.id_user = user.id

    self.__user_chat_repository.add(userChatDTO)

  def update(self, id, chat : ChatVO, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    current_chat : ChatDTO = self.__chat_repository.find(id)
    if current_chat is None:
      raise IndexError("Chat not found")

    if user.id != current_chat.id_owner:
      raise PermissionError("You are not the owner of this chat")
    
    self.__chat_repository.update(id, chat.to_dto())

  def remove_chat(self, id, user_id):
    user : UserDTO = self.__user_repository.find(user_id)

    chat : ChatDTO = self.__chat_repository.find(id)
    if chat is None:
      raise IndexError("Chat not found")
    
    if user.id != chat.id_owner:
      raise PermissionError("You are not the owner of this chat")
    
    self.__message_repository.delete_by_chat(chat.id)
    self.__user_chat_repository.delete_by_chat(chat.id)
    self.__chat_repository.delete(chat)

  def leave_chat(self, id, user_id):
    user : UserDTO = self.__user_repository.find(user_id)
    
    chat : ChatDTO = self.__chat_repository.find(id)
    if chat is None:
      raise IndexError("Chat not found")

    if self.__user_chat_repository.find_by_user_and_chat(user.id, chat.id) is None:
      raise IndexError("User is not in this chat")
    
    if user.id == chat.id_owner:
      raise Exception("Owner can't leave the chat")

    self.__user_chat_repository.remove_by_user_and_chat(user.id, chat.id)
    
  def admin_remove_user_from_chat(self, chat_id, user_id, admin_id):
    user_to_delete : UserDTO = self.__user_repository.find(user_id)
    if user_to_delete is None:
      raise IndexError("Informed User not found")

    chat : ChatDTO = self.__chat_repository.find(chat_id)
    if chat is None:
      raise IndexError("Chat not found")
    
    if admin_id != chat.id_owner:
      raise PermissionError("You are not the owner of this chat")

    if self.__user_chat_repository.find_by_user_and_chat(admin_id, chat.id) is None:
      raise Exception("You are not in this chat")

    if self.__user_chat_repository.find_by_user_and_chat(user_to_delete.id, chat.id) is None:
      raise IndexError("Informed User is not in this chat")
    
    if user_to_delete.id == chat.id_owner:
      raise Exception("Owner cannot be removed from the chat")

    self.__user_chat_repository.remove_by_user_and_chat(user_to_delete.id, chat.id)    