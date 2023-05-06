from requests import post, get, put
import json

def get_playlist(token, playlist_id, page):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={page * 50}&limit=50&market=US&locale=en-US,en;q=0.9"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result