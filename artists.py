from requests import post, get, put
import json

def get_top_tracks_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

