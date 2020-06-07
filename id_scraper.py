#!/usr/bin/python3
import requests
import tvdbsimple as tvdb
import re
from bs4 import BeautifulSoup
imdb_key = "imdb key here"
tvdb_key = "tvdb key here"
tvdb.KEYS.API_KEY=tvdb_key

def movie_search():
    try:
        # IMDB SEARCH
        title = requests.utils.quote(input("\n\nTitle: "))
        year = input("Year: ")

        url = "http://www.omdbapi.com/?apikey={}&t={}&type=movie&y={}&plot=short&r=json".format(imdb_key, title, year)
        response = requests.get(url)
        data = response.json()
        print("\nIMDB: " + data["imdbID"])

        # TVDB SEARCH (parses page directly)
        url = "https://thetvdb.com/movies/{}".format(title.replace("%20", "-"))
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        info = soup.find(class_="list-group")
        id = list(info.children)
        idSoup = BeautifulSoup(str(id), "html.parser")
        id_final = idSoup.find("span").text
        print("TVDB: " + str(id_final))

    except Exception as e:
        print(str(e))

def tv_search():
    try:
        # IMDB SEARCH
        title = requests.utils.quote(input("\n\nTitle: "))
        year = input("Year: ")

        url = "http://www.omdbapi.com/?apikey={}&t={}&type=series&y={}&plot=short&r=json".format(imdb_key, title, year)
        response = requests.get(url)
        data = response.json()
        print("\nIMDB: " + data["imdbID"])

        # TVDB SEARCH (uses api)
        search = tvdb.Search()
        response = search.series(imdbId=data["imdbID"])
        print("TVDB: " + str(response[0]["id"]))

    except Exception as e:
        print(str(e))

def game_search():
    try:
        title = input("\n\nTitle: ")
        title = title.replace(" ", "-")
        url = "https://www.igdb.com/games/" + title
        response = requests.get(url).text
        gameID = re.search(r'game_id=\d+', response).group().split("=")[1]
        print("IGDB: " + str(gameID))


    except Exception as e:
        print(str(e))

def main():
    print("\n****** ID SCRAPER ******")
    while True:
        type = input("\nType (m/tv/g): ").upper()
        if type in ["M", "TV", "G"]:
            if type == "M":
                movie_search()
            elif type == "TV":
                tv_search()
            else:
                game_search()
            break
main()
input()
