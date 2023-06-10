def _to_json(vos):
  json = []
  for vo in vos:
    json.append(vo.to_json())

  return json