from repository.base import Base
from sqlalchemy import Column, Sequence, Integer, String, DateTime, ForeignKey

class MessageDTO(Base):
  __tablename__ = "message"

  id = Column(Integer, Sequence("seq_movie_pk"), primary_key=True, autoincrement=True)
  id_chat = Column(Integer, ForeignKey("chat.id"), nullable=False)
  id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
  date = Column(DateTime, nullable=False)
  message = Column(String(400), nullable=False)