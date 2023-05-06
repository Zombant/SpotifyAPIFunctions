import os
import base64
from requests import post, get
import json
import random
import string
import hashlib
import webbrowser
import socket
from urllib import parse

from secrets import *

port = 8080
redirect_uri = f'http://localhost:{port}'

def random_string(len):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(len))

# Returns base 64 encoding of the hash of the code_verifier (which is a random string)
def generate_code_challenge(code_verifier):
    m = hashlib.sha256()
    m.update(code_verifier.encode())
    return base64.b64encode(m.digest())

# Prompt user to sign in and returns a token
def authorize():
    # Generate a random string
    code_verifier = random_string(128)

    # Generate authentication URL and open browser to authentication window
    state = random_string(16)
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private'

    args = f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}&scope={scope}&code_challenge_method=S256&code_challenge={generate_code_challenge(code_verifier).decode().replace('+', '-').replace('/', '_').replace('=', '')}"
    url = "https://accounts.spotify.com/authorize" + args
    webbrowser.open(url)

    # Open a socket to listen for callback
    s = socket.socket()
    s.bind(('localhost', port))
    s.listen(1)
    conn, addr = s.accept()

    # Get response
    resp = conn.recv(1024).decode()

    # Try to get code from callback url, if it succeeds, close window
    # If it fails, display fail message in browser and return None
    try:
        code = parse.parse_qs(parse.urlparse(resp).query)['code'][0]
        reply = """
HTTP/1.1 200 OK
Content-Type: text/html


<html>
    <head>
        <title>Success</title>
        <script>
            window.close()
        </script>
    </head>
</html>
"""
        conn.sendall(reply.encode())

        conn.close()
        s.close()
    except:
        reply = """
HTTP/1.1 200 OK
Content-Type: text/html


<html>
    <head>
        <title>Fail</title>
    </head>
    <body>
        <p>Failed to get Authentication code</p>
    </body
</html>
"""
        conn.sendall(reply.encode())

        conn.close()
        s.close()
        return None

    
    ### Requesting access token ###
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": code_verifier}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    refresh_token = json_result["refresh_token"]
    return token, refresh_token

def get_new_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    refresh_token = json_result["refresh_token"]
    return token, refresh_token


# Only needed for use without OAuth
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_profile(token):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


# Returns first artist from search
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
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
    headers = get_auth_header(token)
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
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_playlist(token, playlist_id, page):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={page * 50}&limit=50&market=US&locale=en-US,en;q=0.9"
    headers = get_auth_header(token)
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

    print(get_profile(token))

    token, refresh_token = get_new_token(refresh_token)

    print(get_profile(token))

    #token = get_token()

    #print(songs_in_A_and_B(token, pop_id, jiggy_wigs_id))


    # Getting songs of an artist
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
