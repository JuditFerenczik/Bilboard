
import requests
from bs4 import BeautifulSoup
from secretkeys import CLIENT_SECRET,CLIENT_ID, TOKEN
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
URL_REDIRECT = "http://example.com"
spotify_auth = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=URL_REDIRECT,
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path=".cache"
)
spotify_auth.get_access_token(as_dict=False)
s = spotipy.Spotify(oauth_manager=spotify_auth)
yearInQuestion = input("Which year do you want to travel to? Type the date in this form YYYY-mm-dd!")
try:
    datetime.datetime.strptime(yearInQuestion, '%Y-%m-%d')
    URL = f"https://www.billboard.com/charts/hot-100/{yearInQuestion}/"
    print(URL)
    response = requests.get(URL)
    website_html = response.text
    soup = BeautifulSoup(website_html, "html.parser")
    all_bands = soup.select("li.o-chart-results-list__item > span.a-no-trucate")
    all_songs = soup.select("li.o-chart-results-list__item > h3")
    all_bands = [band.getText().strip() for band in all_bands]
    print(len(all_bands))
    # all_bands = [all_bands[i] for i in range(1,len(all_bands), 8)][:-3]
    all_songs = [song.getText().strip() for song in all_songs]
    song_list = [[(i + 1), all_bands[i], all_songs[i]] for i in range(0, len(all_songs))]
    # print(all_songs)
    # print(all_bands)
    print(song_list)
    YYYY = yearInQuestion.split("-")[0]
    song_uris = []
    for i in range(len(all_songs)):
        print(song_list[i][2])
        result = s.search(q=f"track:{song_list[i][2]}  year:{YYYY}", type="track")  # artist:{song_list[i][1]}
        # print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"Couldn't find {all_songs[i][2]}  on Spotify.")
    # print(song_uris)
    user_id = s.current_user()["id"]
    print(user_id)
    playlist = s.user_playlist_create(user=user_id, name=f"{yearInQuestion} Billboard 100", public=False)
    print(playlist)
    s.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
except ValueError:
    print("Input type is not a date!Quiting...")
