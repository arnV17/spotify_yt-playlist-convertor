def get_spotify_auth_url():
    scope = "playlist-read-private"
    return (f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}"
            f"&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}")

def get_spotify_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=token_data).json()
    print(response)  # Debugging: Print the full response
    return response.get('access_token')  # Use .get() to avoid KeyError


def get_spotify_tracks(token, playlist_url):
    try:
        # Extract playlist ID from the URL
        playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        headers = {'Authorization': f'Bearer {token}'}
        
        # Make the API request
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
        response_data = response.json()  # Parse the JSON response
        
        # Debugging: Check the structure of the response
        if 'items' not in response_data:
            print("Response does not contain 'items':", response_data)
            return []

        # Safely extract track names and artist names
        tracks = []
        for item in response_data.get('items', []):
            track = item.get('track', {})
            track_name = track.get('name', 'Unknown Track')
            artist_name = track.get('artists', [{}])[0].get('name', 'Unknown Artist')
            tracks.append(f"{track_name} {artist_name}")
        
        return tracks
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

