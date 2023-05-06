from requests import post, get, put
import json

# Returns profile of signed-in user
def get_current_profile(token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_user_top_tracks(token, type):
    raise NotImplementedError

def get_user_profile(token, user_id):
    raise NotImplementedError

def follow_playlist(token, playlist_id):
    raise NotImplementedError

def unfollow_playlist(token, playlist_id):
    raise NotImplementedError

def get_followed_artists(token):
    raise NotImplementedError

def follow(token, type, ids):
    raise NotImplementedError

def unfollow(token, type, ids):
    raise NotImplementedError

def check_user_follows(token, type, ids):
    raise NotImplementedError

def check_users_follow_playlist(token, playlist_id, ids):
    raise NotImplementedError