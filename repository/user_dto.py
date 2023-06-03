from repository.base import Base
from sqlalchemy import Column, Integer, String, Sequence

class UserDTO(Base):
  __tablename__ = "user"

  id = Column(Integer, Sequence('user_pk_seq'), primary_key=True, autoincrement=True)
  email = Column(String, nullable=False)
  password = Column(String, nullable=False)
  token = Column(String, nullable=False)
  name = Column(String(25), nullable=False)
  description = Column(String(140), nullable=True)