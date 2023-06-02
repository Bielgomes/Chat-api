from repository.db_config import DBConfig
from sqlalchemy.orm import sessionmaker
from typing import TypeVar, Generic

M = TypeVar('M')

class AbstractRepository(Generic[M]):
  _class = None
  _session = None

  def __init__(self, klass):
    _db = DBConfig.create()
    session = sessionmaker(bind=_db.engine)
    self._session = session()
    self._class = klass

  def find_all(self):
    return self._session.query(self._class)

  def find(self, id):
    return self._session.query(self._class).get(id)

  def add(self, model : M):
    self._session.add(model)
    self._session.commit()

  def delete(self, model : M):
    self._session.delete(model)
    self._session.commit()