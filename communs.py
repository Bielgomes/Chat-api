ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def _to_json(vos):
  json = []
  for vo in vos:
    json.append(vo.to_json())

  return json

def _allowed_file(filename):
  return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS