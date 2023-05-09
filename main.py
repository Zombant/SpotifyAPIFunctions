from secrets import *

from auth import *

from player import *
from users import *
from search import *
from artists import *
from albums import *
from playlists import *

import argparse
import os


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

def load_token(file):
    with open(file, 'r') as f:
        return f.readlines()[0].replace('\n', '')

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-a", "--create-token", required=False, action='store_true', help="Request and store a new token by logging in user")
    arg_parser.add_argument("-b", "--refresh-token", required=False, action='store_true', help="Refresh stored token")
    arg_parser.add_argument("-c", "--pause", required=False, action='store_true', help="Pause playback")
    arg_parser.add_argument("-d", "--play", required=False, action='store_true', help="Resume playback")
    arg_parser.add_argument("-e", "--toggle", required=False, action='store_true', help="Toggle playback")
    arg_parser.add_argument("-f", "--is-playing", required=False, action='store_true', help="Return True if player is playing")
    arg_parser.add_argument("-g", "--next", required=False, action='store_true', help="Next track")
    arg_parser.add_argument("-i", "--previous", required=False, action='store_true', help="Previous track")
    arg_parser.add_argument("-j", "--list-devices", required=False, action='store_true', help="List available devices")
    arg_parser.add_argument("-k", "--transfer-playback", required=False, action='store', help="Transfer playback to another device")
    arg_parser.add_argument("-l", "--current-device", required=False, action='store_true', help="Get the name and id of the current device")
    arg_parser.add_argument("-m", "--current-track", required=False, action='store_true', help="Get the currently playing track")


    args = arg_parser.parse_args()

    # TODO: Don't store tokens in plain text
    token_file = os.path.expanduser('~') + '/.local/share/spotify_tokens'

    if args.create_token:
        token, refresh_token = get_auth_token()
        with open(token_file, 'w+') as f:
            f.write(f'{token}\n\n{refresh_token}')
        exit()
    
    if args.refresh_token:
        refresh_token = ''
        with open(token_file, 'r') as f:
            refresh_token = f.readlines()[-1]

        token, refresh_token = get_new_token(refresh_token)

        with open(token_file, 'w+') as f:
            f.write(f'{token}\n\n{refresh_token}')
        exit()
    
    if args.pause:
        pause_playback(load_token(token_file))
        exit()

    if args.play:
        resume_playback(load_token(token_file))
        exit()

    if args.toggle:
        try:
            is_playing = get_playback_state(load_token(token_file))['is_playing']
        except:
            is_playing = None
            print('Could not toggle')
        if is_playing == True:
            pause_playback(load_token(token_file))
        elif is_playing == False:
            resume_playback(load_token(token_file))
        exit()

    if args.is_playing:
        try:
            print(get_playback_state(load_token(token_file))['is_playing'])
        except:
            print('Could not get playback state')
            exit()

    if args.next:
        next_track(load_token(token_file))
        exit()

    if args.previous:
        previous_track(load_token(token_file))
        exit()

    if args.list_devices:
        devices = get_available_devices(load_token(token_file))['devices']
        for i, device in enumerate(devices):
            print(f"{device['name']} - {device['id']}")
        exit()

    if args.transfer_playback != None:
        transfer_playback(load_token(token_file), args.transfer_playback, False)
        exit()

    if args.current_track:
        track = get_current_track(load_token(token_file))
        for i in range(0, len(track['item']['artists'])):
            print(f"Artist: {track['item']['artists'][i]['name']}")
        print(f"Track: {track['item']['name']}")
        print(f"Album: {track['item']['album']['name']}")
        exit()

    if args.current_device:
        playback_state = get_playback_state(load_token(token_file))
        print(f"{playback_state['device']['name']} - {playback_state['device']['id']}")
        exit()