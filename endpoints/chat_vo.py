from repository.chat_dto import ChatDTO

class ChatVO:   
  def __init__(self):
    self.id = None
    self.id_owner = None
    self.name = "",
    self.description = "",
    self.max_users = 0

  def _is_string_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or not (json[att_name].strip()) or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]
  
  def _is_description_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]
  
  def _is_max_users_valid(self, json, att_name):
    if att_name not in json or json[att_name] is None or json[att_name] < 2 or json[att_name] > 50:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]

  @staticmethod
  def from_dto(dto : ChatDTO):
    vo = ChatVO()
    vo.id = dto.id
    vo.id_owner = dto.id_owner
    vo.name = dto.name
    vo.description = dto.description
    vo.max_users = dto.max_users

    return vo
  
  def from_json(self, json):
    self.name = self._is_string_valid(json, "name", 25)
    self.description = self._is_description_valid(json, "description", 140)
    self.max_users = self._is_max_users_valid(json, "max_users")

  def to_dto(self):
    dto = ChatDTO()
    dto.id = self.id
    dto.id_owner = self.id_owner
    dto.name = self.name
    dto.description = self.description
    dto.max_users = self.max_users
    
    return dto

  def to_json(self):
    return self.__dict__.copy()