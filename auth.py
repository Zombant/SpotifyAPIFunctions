import hashlib
import webbrowser
import socket
import random
import string
import base64
import json
from requests import post, get, put
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
def get_auth_token():
    # Generate a random string
    code_verifier = random_string(128)

    # Generate authentication URL and open browser to authentication window
    state = random_string(16)
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-recently-played'

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

# Usage: new_token, new_refresh_token = get_new_token(old_refresh_token)
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
def get_standard_token():
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
