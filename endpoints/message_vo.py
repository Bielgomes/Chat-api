from repository.message_dto import MessageDTO

class MessageVO:
  def __init__(self):
    self.id = None
    self.id_user = None
    self.id_chat = None
    self.date = None
    self.message = ""

  def _is_message_valid(self, json, att_name, max_length):
    if att_name not in json or json[att_name] is None or len(json[att_name]) > max_length:
      raise ValueError(f"The attribute {att_name} is invalid!")
    return json[att_name]

  @staticmethod
  def from_dto(dto : MessageDTO):
    vo = MessageVO()
    vo.id = dto.id
    vo.id_user = dto.id_user
    vo.id_chat = dto.id_chat
    vo.date = dto.date
    vo.message = dto.message

    return vo

  def from_json(self, json):
    self.message = self._is_message_valid(json, "message", 400)

  def to_dto(self):
    dto = MessageDTO()
    dto.id = self.id
    dto.id_user = self.id_user
    dto.id_chat = self.id_chat
    dto.date = self.date
    dto.message = self.message

    return dto

  def to_json(self):
    json = self.__dict__.copy()
    json["date"] = str(json["date"])
    
    return json