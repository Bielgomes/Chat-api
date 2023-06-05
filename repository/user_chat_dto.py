from repository.base import Base
from sqlalchemy import Column, Sequence, Integer, ForeignKey

class UserChatDTO(Base):
  __tablename__ = "userchat"

  id = Column(Integer, Sequence("userchat_pk_seq"), primary_key=True, autoincrement=True)
  id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
  id_chat = Column(Integer, ForeignKey("chat.id"), nullable=False)