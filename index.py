from pty import slave_open
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import re

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1081 Yowser/2.5 Safari/537.36"}

def get_url():
  for count in range(1, 3):
    url = 'https://yummyanime.org/page/' + str(count)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml") #html.parser
    data = soup.find_all("a", class_="poster grid-item d-flex fd-column has-overlay")
    for i in data:
      card_url = i.get("href")
      yield card_url

for card_url in get_url():
  sleep(2)
  responseUnix = requests.get('https://www.unixtimestamp.com/', headers=headers)
  soupUnix = BeautifulSoup(responseUnix.text)
  response = requests.get(card_url, headers=headers)
  soup = BeautifulSoup(response.text)

  unixTime = soupUnix.find("div", class_='value epoch').text
  anime_score = soup.find('div', 'ratingscore-anime').text.split(' ', 1)[0]
  anime_frame = soup.find('iframe').get("src")
  anime_tittle_ru = soup.find("h1").text
  anime_tittle_en = soup.find("div", class_='pmovie__original-title').text
  anime_sheets = soup.find('header', class_='page__subcol-main flex-grow-1 d-flex fd-column')
  anime_status = anime_sheets.find('a').text
  anime_episod_last = anime_sheets.select_one('.pmovie__genres:nth-child(2) > .anime-r').text.split(' ', 1)[0]
  anime_episod_all = anime_sheets.select_one('.pmovie__genres:nth-child(2) > .anime-r').text.partition(' ')[2][3:]
  anime_season = anime_sheets.select_one('.pmovie__genres:nth-child(3) > .anime-r > a').text
  anime_type = anime_sheets.select_one('.pmovie__genres:nth-child(4) > .anime-r > a').text
  anime_genre = anime_sheets.select_one('.pmovie__genres:nth-child(5) > .anime-r').text
  anime_studio = anime_sheets.select_one('.pmovie__genres:nth-child(6) > .anime-r').text
  anime_translate = anime_sheets.select_one('.pmovie__genres:nth-child(7) > .anime-r').text
  anime_cover = 'https://yummyanime.org' + soup.select_one('.pmovie__poster > img').get('data-src')
  anime_desc = soup.find('div', class_='page__text full-text clearfix').text


  print(unixTime + '\n' +anime_tittle_ru + '\n' + anime_tittle_en + '\n' + anime_status + '\n' + anime_episod_last + '\n' + anime_episod_all + '\n' + anime_season +  '\n' + anime_type +  '\n' + anime_genre +  '\n' + anime_studio +  '\n' + anime_translate +  '\n' + anime_score +  '\n' + anime_frame +  '\n' + anime_cover +  '\n' + anime_desc + '\n\n')