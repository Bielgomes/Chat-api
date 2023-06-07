from repository.chat_repository import ChatRepository
from repository.user_repository import UserRepository
from repository.user_chat_repository import UserChatRepository
from repository.user_dto import UserDTO
from repository.chat_dto import ChatDTO
from repository.user_chat_dto import UserChatDTO
from endpoints.chat_vo import ChatVO

class ChatService:
  __chat_repository = ChatRepository()
  __user_repository = UserRepository()
  __user_chat_repository = UserChatRepository()

  def find_chat(self, id, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if not user:
      raise IndexError("User not found")

    chat : ChatDTO = self.__chat_repository.find(id)
    if not chat:
      raise IndexError("Chat not found")
    
    userChatDTO : UserChatDTO = self.__user_chat_repository.find_by_user_and_chat(user.id, chat.id)
    if userChatDTO:
      raise Exception("User already in this chat")
    
    return ChatVO.from_dto(chat)

  def create_chat(self, chat : ChatVO, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if not user:
      raise IndexError("User not found")

    chatDTO = chat.to_dto()
    chatDTO.id_owner = user.id

    userChatDTO = UserChatDTO()
    userChatDTO.id_user = user.id

    chat_id = self.__chat_repository.add(chatDTO)
    userChatDTO.id_chat = chat_id
    self.__user_chat_repository.add(userChatDTO)

  def join_chat(self, id, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if not user:
      raise IndexError("User not found")
    
    chat : ChatDTO = self.__chat_repository.find(id)
    if not chat:
      raise IndexError("Chat not found")
    
    userChatDTO : UserChatDTO = self.__user_chat_repository.find_by_user_and_chat(user.id, chat.id)
    if userChatDTO:
      raise Exception("User already in this chat")
    
    userChatDTO = UserChatDTO()
    userChatDTO.id_chat = chat.id
    userChatDTO.id_user = user.id

    self.__user_chat_repository.add(userChatDTO)

  def update(self, id, chat : ChatVO, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if not user:
      raise IndexError("User not found")
    
    current_chat : ChatDTO = self.__chat_repository.find(id)
    if not current_chat:
      raise IndexError("Chat not found")

    if user.id != current_chat.id_owner:
      raise Exception("You are not the owner of this chat")
    
    self.__chat_repository.update(id, chat.to_dto())

  def remove_chat(self, id, token):
    user : UserDTO = self.__user_repository.find_by_token(token)
    if not user:
      raise IndexError("User not found")

    chat : ChatDTO = self.__chat_repository.find(id)
    if not chat:
      raise IndexError("Chat not found")
    
    if user.id != chat.id_owner:
      raise Exception("You are not the owner of this chat")
    
    self.__chat_repository.delete(chat)