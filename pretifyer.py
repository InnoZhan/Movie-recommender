import json
import re
movies = {}

with open("new_data_file.json", "r") as myfile:
    movies = json.loads(myfile.read())
    for movie in movies:
        movies[movie]['summary'] = " ".join(movies[movie]['summary'].split())

with open("new_data_file.json", "w") as write_file:
    json.dump(movies, write_file)
