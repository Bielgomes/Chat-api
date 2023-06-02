import re
from repository.user_dto import UserDTO

class UserVO():
  __regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

  def __init__(self):
    self.id = None,
    self.email = "",
    self.password = "",
    self.token = ""

  def _is_email_valid(self, json, att_name):
    if att_name not in json or json[att_name] is None or not json[att_name].strip() or not self.__regex.fullmatch(json[att_name]):
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]

  def _is_string_valid(self, json, att_name):
    if att_name not in json or json[att_name] is None or not json[att_name].strip():
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]

  def fromJson(self, json):
    self.email = self._is_email_valid(json, "email"),
    self.password = self._is_string_valid(json, "password")

  @staticmethod
  def fromDto(self, dto : UserDTO):
    vo = UserVO()
    vo.id = dto.id
    vo.email = dto.email
    vo.password = dto.password
    vo.token = dto.token
    
    return vo

  def to_dto(self):
    dto = UserDTO()
    dto.id = self.id
    dto.email = self.email
    dto.password = self.password
    dto.token = self.token

    return dto

  def to_json(self):
    return self.__dict__.copy()