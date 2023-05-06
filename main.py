from secrets import *

from auth import *

from player import *
from users import *
from search import *
from artists import *
from albums import *
from playlists import *


def get_playlist_items(token, playlist_id):
    playlist_items = []
    
    songs = get_playlist(token, playlist_id, 0)
    playlist_size = songs['total']
    
    page = 0
    while len(playlist_items) < playlist_size:
        songs = get_playlist(token, playlist_id, page)
        for i, song in enumerate(songs['items']):
            playlist_items.append({
                'id': songs['items'][i]['track']['id'],
                'name': songs['items'][i]['track']['name'],
                'artist': songs['items'][i]['track']['artists'][0]['name']
            })
        page += 1
    
    return playlist_items

def print_playlist(token, playlist_id):
    for i, song in enumerate(get_playlist_items(token, playlist_id)):
        print(f"{i}. {song}")
        
def songs_in_A_not_in_B(token, playlist_a_id, playlist_b_id):
    playlist_a = get_playlist_items(token, playlist_a_id)
    playlist_b = get_playlist_items(token, playlist_b_id)
    return [item for item in playlist_a if item not in playlist_b]

def songs_in_A_and_B(token, playlist_a_id, playlist_b_id):
    playlist_a = get_playlist_items(token, playlist_a_id)
    playlist_b = get_playlist_items(token, playlist_b_id)
    return [item for item in playlist_a if item in playlist_b]

if __name__ == "__main__":
    token, refresh_token = authorize()
