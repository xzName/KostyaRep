from bs4 import BeautifulSoup
import requests
import re
import csv
import random as r


# constants
URL = 'https://songdata.io/charts/united-states'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
           'accept': '*/*'}
GENRES = ['dance pop', 'pop', 'latin', 'edm', 'canadian hip hop',
          'panamanian pop', 'electropop', 'reggaeton flow', 'canadian pop',
          'reggaeton', 'dfw rap', 'brostep', 'country rap', 'escape room',
          'trap music', 'big room', 'boy band', 'pop house', 'australian pop',
          'r&b en espanol', 'atl hip hop', 'rap']

pattern = r'[0-9]+'
def get_html(url, headers=''):
    session = requests.Session()
    resp = session.get(url, headers=headers)
    return resp


def get_music_info(url, music_info):
    html_code = get_html(url).text

    soup = BeautifulSoup(html_code, 'html.parser')

    # getting links
    song_analysis = soup.find_all('div', class_='progress-wrapper')
    music_info_lst = []
    for song_data in song_analysis:
        music_info_lst.append(song_data.find('div', class_='progress-percentage').find('span').text[:-1])


    # getting song information
    popul_text = soup.find('div', 'row justify-content-center').find('div', id='popularity').\
        find('div', class_='progress-bar bg-white').get('style')
    lenght = soup.find('div', class_='col-md-2 text-center').find_all('p')[1].text.split(':')
    length_sec = int(lenght[0]) * 60 + int(lenght[1])
    music_info.append({
        'author': soup.find('div', class_='col-lg-6').find('h2').text,
        'song': soup.find('div', class_='col-lg-6').find('h1').text,
        'length': str(length_sec),
        'loudness': soup.find('div', 'row justify-content-center').find('div', id='loudness').find_all('p')[1].text[
                    :-3].split('.')[0],
        'acousticness': '1' if music_info_lst[0] == '0' else music_info_lst[0],
        'bpm': soup.find('div', class_='col-lg-4 text-center').find_all('div', class_='display-4 mb-0 text-white')[-1].text,
        'energy': music_info_lst[1],
        'danceability': music_info_lst[4],
        'liveness': music_info_lst[2],
        'valence': music_info_lst[7],
        'speechiness': music_info_lst[3],
        'popularity': '1' if re.findall(pattern, popul_text)[0] == '0' else re.findall(pattern, popul_text)[0],
        'genres': GENRES[r.randint(0,21)]})


    return music_info

# Saving data to csv file
# data - data from web page
# file_name - name of file to saving
def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as f:
        wrt = csv.writer(f, delimiter=',')
        wrt.writerow(['Track.Name', 'Artist.Name', 'Genre', 'Beats.Per.Minute', 'Energy', 'Danceability', 'Loudness..dB..', 'Liveness', 'Valence.', 'Length.', 'Acousticness..', 'Speechiness.', 'Popularity'])
        for item in data:
            wrt.writerow([item['song'], item['author'],item['genres'] ,item['bpm'], item['energy'], item['danceability'], item['loudness'], item['liveness'], item['valence'], item['length'], item['acousticness'], item['speechiness'], item['popularity']])


def parse_songdata(url):
    html_code = get_html(url, headers=HEADERS).text

    soup = BeautifulSoup(html_code, 'html.parser')
    links = soup.find_all('tr', class_='clickable-row')

    # getting link of a song
    link_lst = []
    for link in links:
        link_lst.append('https://songdata.io' + link.find('a').get('href'))

    # finding information of music
    music_info = []
    for link in link_lst:
        music_info = get_music_info(link, music_info)

    print(music_info)

    save_to_csv(music_info, 'data.csv')


#URL = input()
parse_songdata(URL)
