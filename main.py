from requests import post, get, put
import json

from secrets import *
from auth import *
from player import *
from users import *


# Returns first artist from search
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

# Returns first album from search
def search_for_album(token, album_name):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={album_name}&type=album&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    if len(json_result) == 0:
        print("No album with this name exists...")
        return None
    
    return json_result[0]

def get_top_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?country=US"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_playlist(token, playlist_id, page):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={page * 50}&limit=50&market=US&locale=en-US,en;q=0.9"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

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
    
    print(get_available_devices(token))

    

    #token, refresh_token = get_new_token(refresh_token)
    #print(get_profile(token))

    #token = get_token()

    #print(songs_in_A_and_B(token, pop_id, jiggy_wigs_id))


    # Getting songs of an artists
    #token = get_token()
    #result = search_for_artist(token, "ACDC")
    #artist_id = result["id"]
    #songs = get_top_songs_by_artist(token, artist_id)
    #for idx, song in enumerate(songs):
    #    print(f"{idx + 1}. {song['name']}")

    # Getting songs of an album
    #token = get_token()
    #result = search_for_album(token, "Wish you were here")
    #album_id = result["id"]
    #songs_in_album = get_album_tracks(token, album_id)
    #print(songs_in_album[0]["artists"][0]["name"])
    #for idx, song in enumerate(songs_in_album):
    #    print(f"{idx + 1}. {song['name']}")
