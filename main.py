
import requests
from bs4 import BeautifulSoup
from secretkeys import CLIENT_SECRET,CLIENT_ID
yearInQuestion = input("Which year do you want to travel to? Type the date in this form YYYY-mm-dd!")

URL = f"https://www.billboard.com/charts/hot-100/{yearInQuestion}/"
print(URL)
response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

#all_songs = soup.find_all(name="li", class_="o-chart-results-list__item")
all_bands = soup.select("li.o-chart-results-list__item > span.a-no-trucate")
all_songs = soup.select("li.o-chart-results-list__item > h3")
all_bands = [band.getText().strip() for band in all_bands]
print(len(all_bands))
#all_bands = [all_bands[i] for i in range(1,len(all_bands), 8)][:-3]
all_songs = [song.getText().strip() for song in all_songs]
song_list = [[(i+1), all_bands[i], all_songs[i]] for i in range(0,len(all_songs))]
#print(all_songs)
#print(all_bands)
print(song_list)
#all_songs = [song.getText() for song in all_songs.find(name="span", class_="c-label")]
#print(all_songs)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                         client_secret=CLIENT_SECRET))
searched_word ="artist:"+ song_list[0][1].replace(" ", "%20") + "+track:" + song_list[0][2].replace(" ", "%20")
#track:Doxy+artist:Miles%20Davis
#searched_word ="remaster%20track:Doxy+artist:Miles%20Davis"
print(searched_word)
results = sp.search(q=searched_word, limit=20)
print(results)