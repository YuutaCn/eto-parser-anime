from dataclasses import replace
import requests
from bs4 import BeautifulSoup
from time import sleep
import lxml

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1081 Yowser/2.5 Safari/537.36"}
id = 0

def get_url():
  for count in range(1, 3):
    url = f'https://yummyanime.org/page/{str(count)}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser") #html.parser
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
  id = id + 1
  unixTime = soupUnix.find("div", class_='value epoch').text.replace('\n', '').replace('\t', '')
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

  print(str(id) + '\n' + unixTime + '\n' +anime_tittle_ru + '\n' + anime_tittle_en + '\n' + anime_status + '\n' + anime_episod_last + '\n' + anime_episod_all + '\n' + anime_season +  '\n' + anime_type +  '\n' + anime_genre +  '\n' + anime_studio +  '\n' + anime_translate +  '\n' + anime_score +  '\n' + anime_frame +  '\n' + anime_cover +  '\n' + anime_desc + '\n\n')

  with open(f'{str(id)}.html', 'w') as html:
    html.write('''<!DOCTYPE html><html lang="ru" class="page">@include('../partials/anime/head-anime.html',{title})<div class="main__container container">"""
    @include('../partials/aside-nav.html')
    <div class="main__content">
      <section class="anime-page">
        <div class="anime-page__tittle">
          <h2 class="anime-page__tittle-ru"></h2>
          <h3 class="anime-page__tittle-en"></h3>
        </div>
        <div class="anime-page__short">
          <picture>
            <img loading="lazy" src="../"
              class="image anime-page__short-cover" width="275" height="380" alt="обложка аниме">
          </picture>
          <div class="anime-page__short-sheet">
            <ul class="anime-page__short-sheet-list list-reset">
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Статус:</span>
                <a class="anime-page__short-sheet-list-item-status anime-sheet-text link t-cap"
                  href="#no-scrolling"></a>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Эпизод:</span>
                <span class="anime-page__short-sheet-list-item-ep anime-sheet-text"></span>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Сезон:</span>
                <a class="anime-page__short-sheet-list-item-season anime-sheet-text link t-cap" href="#no-scrolling"></a>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Тип:</span>
                <a class="anime-page__short-sheet-list-item-type anime-sheet-text link" href="#no-scrolling"></a>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Жанр:</span>
                <ul class="anime-page__short-sheet-list-item-genre list-reset anime-sheet-text li-link t-cap">
                </ul>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Студия:</span>
                <a class="anime-page__short-sheet-list-item-studio anime-sheet-text link" href="#no-scrolling"></a>
              </li>
              <li class="anime-page__short-sheet-list-item">
                <span class="anime-page__short-sheet-list-item-name">Озвучка:</span>
                <ul class="anime-page__short-sheet-list-item-translate list-reset anime-sheet-text li-link">
                </ul>
              </li>
            </ul>
          </div>
        </div>
        <div class="anime-page__desc">
          <h4 class="anime-page__desc-tittle">Описание аниме «<span class="anime-page__desc-tittle-anime"></span>»</h4>
          <p class="anime-page__desc-text"></p>
        </div>
      </section>
      <h2 class="player-tittle">Смотреть аниме «<span class="player-tittle__anime"></span>» без рекламы</h2>
      <div class="player-light"></div>
      <section class="player">
        <div class="player__header">
          <div class="player__header-btn"><button class="player__header-btn-player-2" name="Плеер">Внешний плеер</button><button class="player__header-btn-light" name="Выключить свет">Выключить свет</button><a class="player__header-btn-prob" href="tg://resolve?domain=yuutacn">Сообщить о проблеме</a></div><div class="player__header-social"><p class="player__header-social-view">Смотрят:&NonBreakingSpace;<spanclass="header__player-social-view-span">0</span>&NonBreakingSpace;анимешников</p></div></div><iframe class="player__video" src="../" width="607"height="360" frameborder="0" AllowFullScreen allow="autoplay *; fullscreen *"></iframe></section></div></div></main>@include('../partials/footer.html')</div></body></html>
    '''.format(title={'title':f'{anime_tittle_ru}'}))

  with open('anime.txt', 'a') as anime_list:
    anime_list.write(str({
      "id": str(id),
      "href": f"../ap/{str(id)}.html",
      "last_upd": unixTime,
      "score": anime_score,
      "frame": anime_frame,
      "chibi": "",
      "name": {
        "ru": anime_tittle_ru,
        "en": anime_tittle_en,
      },
      "series": {
        "all": anime_episod_all,
        "last": anime_episod_last
      },
      "translate": [anime_translate],
      "season": anime_season,
      "status": anime_status,
      "type": anime_type,
      "studio": anime_studio,
      "genre": [anime_genre],
      "cover": anime_cover,
      "desc": anime_desc,
      }))