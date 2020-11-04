import requests
from bs4 import BeautifulSoup
import json


def get_image(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.find("div", class_="poster").find('a')['href']
    page = requests.get("https://www.imdb.com"+link)
    soup = BeautifulSoup(page.content, 'html.parser')
    img = soup.find("div", class_="MediaViewerImagestyles__PortraitContainer-sc-1qk433p-2 gIroZm").find('img')['src']
    return img


def load_movies():
    movies = {}
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("tbody", class_="lister-list")
    results = results.findChildren("tr", recursive=False)
    counter = 0
    for movie in results:
        title = movie.findChildren(class_='titleColumn')[0].find('a').text
        prod = movie.findChildren(class_='titleColumn')[0].find('a')['title']
        rating = movie.findChildren(class_='ratingColumn imdbRating')[0].find('strong').text
        year = movie.findChildren(class_='titleColumn')[0].findChildren(class_='secondaryInfo')[0].text
        img = get_image("https://www.imdb.com" +movie.findChildren(class_='titleColumn')[0].find('a')['href'])
        temp = {
            "img": img,
            "title": title,
            "prod": prod,
            "year": year,
            "rating": rating
        }
        movies[counter] = temp
        print(counter)
        counter += 1
    with open("data_file.json", "w") as write_file:
        json.dump(movies, write_file)
    return movies


def get_movies():
    with open("data_file.json", "r") as myfile:
        movies = json.loads(myfile.read())
        return movies