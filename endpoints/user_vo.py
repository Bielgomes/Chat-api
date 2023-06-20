import re
from repository.user_dto import UserDTO

class UserVO():
  __regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

  def __init__(self):
    self.id = None,
    self.email = "",
    self.password = "",
    self.token = ""
    self.name = ""
    self.description = ""

  def _is_email_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or not json[att_name].strip() or not self.__regex.fullmatch(json[att_name]) or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]

  def _is_string_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or not (json[att_name].strip()) or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]
  
  def _is_description_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]
  
  @staticmethod
  def from_dto(dto : UserDTO):
    vo = UserVO()
    vo.id = dto.id
    vo.email = dto.email
    vo.password = dto.password
    vo.token = dto.token
    vo.name = dto.name
    vo.description = dto.description
    
    return vo
  
  @staticmethod
  def from_dto_partial(dto : UserDTO):
    vo = UserVO()
    vo.id = dto.id
    vo.name = dto.name
    vo.description = dto.description
    
    return vo

  def from_json(self, json):
    self.email = self._is_email_valid(json, "email", 90),
    self.password = self._is_string_valid(json, "password", 30)
    self.name = self._is_string_valid(json, "name", 25)
    self.description = self._is_description_valid(json, "description", 140)

  def from_json_login(self,json):
    self.email = self._is_email_valid(json, "email", 320)
    self.password = self._is_string_valid(json, "password", 30)

  def from_json_info(self, json):
    self.name = self._is_string_valid(json, "name", 25)
    self.description = self._is_description_valid(json, "description", 140)

  def from_json_password(self, json):
    self.password = self._is_string_valid(json, "password", 30)

  def from_json_email(self, json):
    self.email = self._is_email_valid(json, "email", 320)

  def to_dto(self):
    dto = UserDTO()
    dto.email = self.email
    dto.password = self.password
    dto.token = self.token
    dto.name = self.name
    dto.description = self.description

    return dto

  def to_json(self):
    json = {}
    
    json["id"] = self.id
    json["name"] = self.name
    json["description"] = self.description

    return json