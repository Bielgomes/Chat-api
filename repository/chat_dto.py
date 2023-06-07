from repository.base import Base
from sqlalchemy import Column, ForeignKey, Sequence, Integer, String

class ChatDTO(Base):
  __tablename__ = "chat"

  id = Column(Integer, Sequence("chat_pk_seq"), primary_key=True, autoincrement=True)
  id_owner = Column(Integer, ForeignKey("user.id"), nullable=False)
  name = Column(String(25), nullable=False)
  description = Column(String(140), nullable=False)
  max_users = Column(Integer, nullable=False)