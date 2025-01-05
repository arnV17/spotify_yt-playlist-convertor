import requests
from google_auth_oauthlib.flow import InstalledAppFlow

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

playlist_id= None

def authenticate_youtube():
    """
    Simplified function to authenticate the user and obtain an OAuth2 access token.
    """
    # Scopes for YouTube API
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    
    # Start OAuth2 flow and automatically open a browser for authentication
    flow = InstalledAppFlow.from_client_secrets_file(
        "utils/client_secrets.json",  # Path to your OAuth2 credentials JSON file
        scopes=scopes,
    )
    
    # This will handle the authentication in a browser automatically
    credentials = flow.run_local_server(port=0)
    
    return credentials.token  # Return the access token


def create_youtube_playlist(title):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "utils/client_secrets.json"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": "This is a sample playlist description.",
            "tags": [
              "sample playlist",
              "API call"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()
    global playlist_id
    playlist_id=response['id']



def add_tracks_to_youtube(track):
    sngid=[]
    
    for item in track:
        
    
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "utils/client_secrets.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=item, 
            type="video"
        )
        response = request.execute()

        video_id = response['items'][0]['id']['videoId']
        sngid.append(video_id)
        
        
    for id in sngid:
        request_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId":id
            }
        }
    }
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "utils/client_secrets.json"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    # Make the API call to add the video to the playlist
    response = youtube.playlistItems().insert(
        part="snippet",
        body=request_body
    ).execute()
        
            
    
      
    
    
        
    

    
        