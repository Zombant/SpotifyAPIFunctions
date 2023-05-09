from requests import post, get, put
import json

def get_playback_state(token):
    url = "https://api.spotify.com/v1/me/player"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    if result.status_code == 204:
        return "204: Playback not available"
    json_result = json.loads(result.content)
    return json_result

def transfer_playback(token, device_id, play):
    url = f"https://api.spotify.com/v1/me/player"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    data = {'device_ids': [device_id], 'play': str(play).lower()}
    return put(url, headers=headers, data=json.dumps(data)) # can alternatively use json=data

def get_available_devices(token):
    url = "https://api.spotify.com/v1/me/player/devices"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_current_track(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def resume_playback(token):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def pause_playback(token):
    url = "https://api.spotify.com/v1/me/player/pause"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def next_track(token):
    url = "https://api.spotify.com/v1/me/player/next"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def previous_track(token):
    url = "https://api.spotify.com/v1/me/player/previous"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def seek_to_position(token, position_ms):
    url = f"https://api.spotify.com/v1/me/player/seek?position_ms={position_ms}"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

# states are 'track', 'repeat', or 'off'
def set_repeat_mode(token, state):
    url = f"https://api.spotify.com/v1/me/player/repeat?state={state}"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def set_volume(token, volume_percent):
    url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percent}"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

def set_shuffle(token, state):
    url = f"https://api.spotify.com/v1/me/player/shuffle?state={str(state).lower()}"
    headers = {"Authorization": "Bearer " + token}
    return put(url, headers=headers)

# 'after' and 'before' are not implemented
def get_recent_tracks(token, max_items):
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit={max_items}"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_queue(token):
    url = "https://api.spotify.com/v1/me/player/queue"
    headers = {"Authorization": "Bearer " + token}
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def add_to_queue(token, uri):
    url = f"https://api.spotify.com/v1/me/player/queue?uri={uri}"
    headers = {"Authorization": "Bearer " + token}
    return post(url, headers=headers)