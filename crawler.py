from urllib.request import urlopen

import bs4
from PyLyrics import *
from bs4 import BeautifulSoup

BASE_WIKIPEDIA_URL = 'https://en.wikipedia.org'


class Song:
    def __init__(self, name, writers, year, lyrics, url):
        self.name = name
        self.writers = writers
        self.year = year
        self.lyrics = lyrics
        self.url = url


def download_html(url):
    # type: (str) -> BeautifulSoup
    """
    Download html from given url and return BeautifulSoup for parse the html
    :param url: url for the wanted html
    :return: BeautifulSoup object with the downloaded html content
    """
    content = urlopen(url).read()
    return BeautifulSoup(content, 'html.parser')


def parse_song_list(table):
    pass


def get_songs_urls(html_page):
    all_songs_url = html_page.find('div', {'class': 'mw-category'})
    all_songs_url = all_songs_url.find_all('a')
    return [f'{BASE_WIKIPEDIA_URL}{link["href"]}' for link in all_songs_url]


def parse_song_content(song_data, url):
    writers = ''
    year = ''
    lyrics = ''
    name = song_data.find('th').text.replace('"', '')
    trs = song_data.find_all('tr')
    for tr in trs:
        try:
            title = tr.find('th').text.lower()
            if 'songwriter' in title:
                writers = [li.text for li in tr.find('td').find('ul').find_all('li')]
            elif 'recorded' in title:
                year = tr.find('td').text
                break
        except:
            pass
    try:
        lyrics = PyLyrics.getLyrics('Madonna', name)
    except Exception as e:
        pass
    return Song(name, writers, year, lyrics, url), name


def get_list_of_songs_written_by_madonna():
    list_of_songs_written_by_madonna_url = 'https://en.m.wikipedia.org/wiki/Category:Songs_written_by_Madonna_(entertainer)'
    html_page = download_html(list_of_songs_written_by_madonna_url)
    all_songs_urls = get_songs_urls(html_page)
    song_list = []
    song_names = set()
    for song in all_songs_urls:
        song_html = download_html(song)
        song_data = song_html.find('table', {'class': ['infobox', 'veven']})
        parsed_song, name = parse_song_content(song_data, song)
        if name not in song_names:
            song_list.append(parsed_song)
            song_names.add(name)

    for song in song_list:
        with open(f'./madonna/{song.name}.txt', 'w') as outfile:
            json.dump(song.__dict__, outfile)


    # parsed_songs = parse_song_list(table_of_songs)

def get_song_recorded_by_madonna():
    url = 'https://en.wikipedia.org/wiki/List_of_songs_recorded_by_Madonna'
    html_page = download_html(url)
    table = html_page.find('table', class_='plainrowheaders')
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    song_list = []
    song_names = set()
    for row in rows:
        try:
            names = row.find('th').contents
            name_l = []
            for name in names:
                try:
                    name_l.append(name.text)
                except:
                    if type(name) is bs4.element.NavigableString:
                        name_l.append(name)
            name = [name for name in name_l if len(name) > 2][0]
            tds = row.find_all('td')
            writ = tds[0]
            writers_obj = writ.contents
            writers = []
            for writer in writers_obj:
                try:
                    writers.append(writer.text)
                except:
                    if type(writer) is bs4.element.NavigableString:
                        writers.append(writer)
            writers = [writer for writer in writers if len(writer) > 2]
            year = tds[2].text
            lyrics = ''
            try:
                lyrics = PyLyrics.getLyrics('Madonna', name.lower())
            except Exception as e:
                pass
            song = Song(name, writers, year, lyrics, url)
            with open(f'./madonna/{song.name}.txt', 'w') as outfile:
                json.dump(song.__dict__, outfile)
        except Exception as e:
            pass


if __name__ == '__main__':
    get_song_recorded_by_madonna()