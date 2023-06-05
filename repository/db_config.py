from sqlalchemy import create_engine
from repository.base import Base

from repository.user_dto import UserDTO
from repository.chat_dto import ChatDTO
from repository.message_dto import MessageDTO
from repository.user_chat_dto import UserChatDTO

class DBConfig:
  __instance = None

  def __init__(self):
    if DBConfig.__instance is not None:
      raise Exception("This class is a singleton, use DB.create")
    
    DBConfig.__instance = self

    self.engine = self.create_connection()

  def create_connection(self):
    db_string = "postgresql://postgres:admin@localhost:5432/chatapi"
    # db_string = "postgresql://postgres:root@localhost:5432/postgres"
    conn = create_engine(db_string)

    Base.metadata.create_all(conn)

    return conn
  
  @staticmethod
  def create():
    if DBConfig.__instance is None:
      DBConfig()

    return DBConfig.__instance