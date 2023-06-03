def _to_json_from_movies(movies):
  jsonMovies = []
  for m in movies:
    jsonMovies.append(m.toJson())
  return jsonMovies