import json
import requests

token = "773ef8d43c2a8c025e5ced077efa302d"

movies_per_page = 10
max_movies = 10000
max_pages = int(max_movies / movies_per_page)

with open('start_index.txt', 'r') as f:
    start_index = int(f.readline())
end_index = start_index

for page in range(start_index, start_index + max_pages):
	url = "https://api.kinopoisk.cloud/movies/all/page/{}/token/{}".format(
		page,
		token
	)
	# Отправляем запрос о фильме
	req = requests.get(url, params={})
	print(page, req)
	if req.ok:
		# Получаем информацию в виде JSON
		film_info = req.json()

		with open(f'movies/data_{page}.json', 'w') as f:
			json.dump(film_info, f)
		end_index += 1
	else:
		break

with open('start_index.txt', 'w') as f:
    f.write(str(end_index))
